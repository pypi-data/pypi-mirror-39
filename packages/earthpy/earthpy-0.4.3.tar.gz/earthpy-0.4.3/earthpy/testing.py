import os
from glob import glob
import matplotlib.pyplot as plt

import rasterio as rio
import earthpy as et
import earthpy.spatial as es

import numpy as np


# set working directory to your home dir/earth-analytics
os.chdir(os.path.join(et.io.HOME, "earth-analytics"))
import matplotlib as mpl
import contextlib

# Import, stack landsat data (PRE OR POST?? data)
all_landsat_band_paths = glob(
    "data/cold-springs-fire/landsat_collect/LC080340322016070701T1-SC20180214145604/crop/*band*.tif"
)

landsat_pre_out = "data/cold-springs-fire/outputs/landsat_prefire.tif"

band_paths = all_landsat_band_paths
out_path = landsat_pre_out


def stack_raster_tifs(band_paths, out_path):
    """Take a list of raster paths and turn into an ouput raster stack.
    Note that this function depends upon the stack() function to be submitted to rasterio.
    but the stack function ins't stand alone as written
    Parameters
    ----------
    band_paths : list of file paths
        A list with paths to the bands you wish to stack. Bands
        will be stacked in the order given in this list.
    out_path : string
        A path for the output stacked raster file.
    """
    # set default import to read
    kwds = {"mode": "r"}

    if not os.path.exists(os.path.dirname(out_path)):
        raise ValueError("The output directory path that you provided does not exist")

    # the with statement ensures that all files are closed at the end of the with statement
    with contextlib.ExitStack() as context:
        sources = [context.enter_context(rio.open(path, **kwds)) for path in band_paths]

        all_crs_equal = [
            source for source in sources if not source.crs == sources[0].crs
        ]
        if not len(all_crs_equal) == 0:
            raise ValueError("All raster files must be in the same CRS.")

        dest_kwargs = sources[0].meta
        dest_count = sum(src.count for src in sources)
        dest_kwargs["count"] = dest_count

        # save out a stacked gtif file
        with rio.open(out_path, "w", **dest_kwargs) as dest:
            stack(sources, dest)
        dest = rio.open(out_path, "w", **dest_kwargs)
        test = stack(sources, dest)

        if not type(sources[0]) == rio.io.DatasetReader:
            raise ValueError(
                "The sources object should be of type: rasterio.RasterReader"
            )

        for ii, ifile in enumerate(sources):
            bands = sources[ii].read()
            print(bands)
            if bands.ndim != 3:
                bands = bands[np.newaxis, ...]
                print("bigger than 3")
            for band in bands:
                dest.write(band, ii + 1)


# function to be submitted to rasterio
# add unit tests: some are here: https://github.com/mapbox/rasterio/blob/master/rasterio/mask.py
# this function doesn't stand alone because it writes to a open object called in the other function.
def stack(sources, dest):
    """Stack a set of bands into a single file.
    Parameters
    ----------
    sources : list of rasterio dataset objects
        A list with paths to the bands you wish to stack. Objects
        will be stacked in the order provided in this list.
    dest : a rio.open writable object that will store raster data.
    """

    # if not os.path.exists(os.path.dirname(dest)):
    #    raise ValueError("The output directory path that you provided does not exist")

    if not type(sources[0]) == rio.io.DatasetReader:
        raise ValueError("The sources object should be of type: rasterio.RasterReader")

    for ii, ifile in enumerate(sources):
        bands = sources[ii].read()
        if bands.ndim != 3:
            bands = bands[np.newaxis, ...]
        for band in bands:
            dest.write(band, ii + 1)


# Import, stack landsat data (PRE OR POST?? data)
all_landsat_band_paths = glob(
    "data/cold-springs-fire/landsat_collect/LC080340322016070701T1-SC20180214145604/crop/*band*.tif"
)

landsat_pre_out = "data/cold-springs-fire/outputs/landsat_prefire.tif"
# Stack landsat tif files using es.stack_raster_tifs - earthpy

landsat_pre = stack_raster_tifs(all_landsat_band_paths, landsat_pre_out)
landsat_pre


import numpy as np
import pandas as pd
import geopandas as gpd
from matplotlib import pyplot as plt
import time
import os
from geopandas.tools import sjoin

# =============================================================================
#
#
#  Leah's clip functions below
#
#
# =============================================================================


"A module to clip vector data using geopandas"

# Create function to clip point data using geopandas


def clip_points(shp, clip_obj):
    """
    Docs Here
    """

    poly = clip_obj.geometry.unary_union
    return shp[shp.geometry.intersects(poly)]


# Create function to clip line and polygon data using geopandas


def clip_line_poly(shp, clip_obj):
    """
    docs
    """

    # Create a single polygon object for clipping
    poly = clip_obj.geometry.unary_union
    spatial_index = shp.sindex

    # Create a box for the initial intersection
    bbox = poly.bounds
    # Get a list of id's for each road line that overlaps the bounding box and subset the data to just those lines
    sidx = list(spatial_index.intersection(bbox))
    # shp_sub = shp[shp.index.isin(sidx)]
    shp_sub = shp.iloc[sidx]

    # Clip the data - with these data
    clipped = shp_sub.copy()
    clipped["geometry"] = shp_sub.intersection(poly)

    # Return the clipped layer with no null geometry values
    return clipped[clipped.geometry.notnull()]


# Final clip function that handles points, lines and polygons


def clip_shp(shp, clip_obj):
    """
    """
    if shp["geometry"].iloc[0].type == "Point":
        return clip_points(shp, clip_obj)
    else:
        return clip_line_poly(shp, clip_obj)


# =============================================================================
#
#
#   comparisons below
#
#
# =============================================================================

cwd = os.getcwd()
wd = "/home/msistaff/jathomps/projects/earth_lab/clip_working/"
if not (cwd) in wd:
    os.chdir(wd)
print(os.getcwd())

shpDir = "/home/msistaff/jathomps/projects/earth_lab/clip_working/shapefiles/"
countIn = "counties/2_counties.shp"
roadsIn = "roads/roads.shp"

shpCounty = gpd.read_file(shpDir + countIn)
shpRoads = gpd.read_file(shpDir + roadsIn)

roiName = "Trinity"

countySel = shpCounty.loc[shpCounty.NAME == roiName]

[sTime, sClock] = time.time(), time.clock()

clip_fun_ret = clip_line_poly(shp=shpRoads, clip_obj=countySel)

[eTime, eClock] = time.time(), time.clock()
print("proc times Leah original clip:", eTime - sTime, eClock - sClock)


[sTime, sClock] = time.time(), time.clock()

intersect = sjoin(shpRoads, countySel, how="inner", op="intersects")
poly = countySel.iloc[0]["geometry"]
# shp_sub = shpRoads.iloc[intersect.index]
clipped = intersect.copy()
clipped["geometry"] = intersect.intersection(poly)

[eTime, eClock] = time.time(), time.clock()
print("proc times sjoin based clip:", eTime - sTime, eClock - sClock)

# within = sjoin(intersect,countySel,how='inner',op='within')

poly_plot = countySel.plot(color="white", edgecolor="blue")
clipped.plot(ax=poly_plot, color="red")

poly_plot2 = countySel.plot(color="white", edgecolor="blue")
clip_fun_ret.plot(ax=poly_plot2, color="red")
