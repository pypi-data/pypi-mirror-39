# scale an input array-like to a mininum and maximum number
# the input array must be of a floating point array
# if you have a non-floating point array, convert to floating using `astype('float')`
# this works with n-dimensional arrays
# it will mutate in place
# min and max can be integers
# may end up deprecating this
def scale_range (input_array, min, max, clip=True):
    # coerce to float if int
    if input_array.dtype == "int":
        input_array = input_array.astype(np.float16)

    input_array += -(np.min(input_array))
    input_array /= np.max(input_array) / (max - min)
    input_array += min
    # if the data have negative values that the user wishes to clip, clip them
    if clip:
        input_array.clip(min, max)
    return ((input_array+ 0.5).astype(np.int8))


"""File Input/Output utilities."""

from download import download
import os.path as op
import os
import matplotlib.pyplot as plt

# plt.style.use('ggplot')

# i believe this is deprecated
#DATA_URLS = {
#    'week_02': [('https://ndownloader.figshare.com/files/7010681',
#                 'boulder-precip.csv'),
#                ('https://ndownloader.figshare.com/files/7010681',
#                 'temperature_example.csv')],
#    'week_02-hw': ('https://ndownloader.figshare.com/files/7426738', 'ZIPFILE'),
#    'week_03': ('https://ndownloader.figshare.com/files/7446715', 'ZIPFILE'),
#    'week_04': ('https://ndownloader.figshare.com/files/7525363', 'ZIPFILE'),
#    'week_05': ('https://ndownloader.figshare.com/files/7525363', 'ZIPFILE'),
#    'week_07': [('https://ndownloader.figshare.com/files/7677208', 'ZIPFILE')]
#}

#               destfile = "data/boulder-precip.csv"'}
HOME = op.join(op.expanduser('~'))
DATA_NAME = op.join('earth-analytics', 'data')
path = None

#def __init__(self, path=None):
    if path is None:
        path = op.join(HOME, DATA_NAME)
    path = path
    data_keys = list(DATA_URLS.keys())


#def __repr__(self):
    s = 'Available Datasets: {}'.format(data_keys)
    #return s

def get_data(self, key=None, name=None, replace=False, zipfile=True):
    """
    Retrieve the data for a given week and return its path.

    This will retrieve data from the internet if it isn't already
    downloaded, otherwise it will only return a path to that dataset.

    Parameters
    ----------
    key : str
        The dataset to retrieve. Possible options can be found in
        ``self.data_keys``.
    replace : bool
        Whether to replace the data for this key if it is
        already downloaded.
    zipfile : bool
        Whether the dataset is a zip file.

    Returns
    -------
    path_data : str
        The path to the downloaded data.
    """
    # alt+shift+e to run
    key=None
    # ok this checks to ensure hte data selected is one available in the dictionary
    if key is None:
        print('Available datasets: {}'.format(
            list(DATA_URLS.keys())))
    elif key not in DATA_URLS:
        raise ValueError("Don't understand key "
                         "{}\nChoose one of {}".format(
            key, DATA_URLS.keys()))
    # if the key is found... get the data

    key = "week_02-hw"
    else:
        this_data = DATA_URLS[key]
        if not isinstance(this_data, list):
            this_data = [this_data]
        data_paths = []
        for url, name in this_data:
            name = key if name is None else name
            if zipfile is True:
                # could this be if name = "ZIPFILE" ??
                name = key
                this_root = path
                this_path = download(url,
                                     path=os.path.join(this_root, name),
                                     replace=replace, kind='zip',
                                     verbose=False)
            else:
                this_root = op.join(self.path, key)
                this_path = download(url, os.path.join(this_root, name),
                                     replace=replace,
                                     verbose=False)
            # this_path = download(url, os.path.join(this_root, name),
            #                     replace=replace, zipfile=zipfile,
            #                     verbose=False)
            data_paths.append(this_path)
        if len(data_paths) == 1:
            data_paths = data_paths[0]
        return data_paths


def bounds_to_box(left, right, bottom, top):
    """Convert bounds to a shapely box.

    This is useful for cropping a raster image.
    """
    box = [(left, bottom), (left, top), (right, top), (right, bottom)]
    box = Polygon(box)
    return box

def crop_image_deprecate(path, geoms, path_out=None):
    """Crop a single file using geometry objects.

    Parameters
    ----------
    path : str
        The path to the raster file to crop
    geoms : list of polygons
        Polygons are GeoJSON-like dicts specifying the boundaries of features
        in the raster to be kept. All data outside of specified polygons
        will be set to nodata.
    path_out : str | None
        The path to the file to be written to disk. If `None`, the input
        path will be overwritten.
    """
    # Mask the input image and update the metadata
    with rio.open(path) as src:
        out_image, out_transform = rio.mask.mask(src, geoms, crop = True)
        out_meta = src.meta.copy()
    out_meta.update({"driver": "GTiff",
                    "height": out_image.shape[1],
                    "width": out_image.shape[2],
                    "transform": out_transform})

    # Write to a new raster file
    if path_out is None:
        path_out = path
    with rio.open(path_out, "w", **out_meta) as dest:
        dest.write(out_image)

# to be deprecated potentially
def stack_deprecate(band_paths, out_path, return_raster=True):
    """Stack a set of bands into a single file.

    Parameters
    ----------
    bands : list of file paths
        A list with paths to the bands you wish to stack. Bands
        will be stacked in the order given in this list.
    out_path : string
        A path for the output file.
    return_raster : bool
        Whether to return a refernce to the opened output
        raster file.
    """
    # Read in metadata
    first_band = rio.open(band_paths[0], 'r')
    meta = first_band.meta.copy()

    # Replace metadata with new count
    counts = 0
    for ifile in band_paths:
        with rio.open(ifile, 'r') as ff:
            counts += ff.meta['count']
    meta.update(count=counts)

    # create a new file
    with rio.open(out_path, 'w', **meta) as ff:
        for ii, ifile in tqdm(enumerate(band_paths)):
            bands = rio.open(ifile, 'r').read()
            if bands.ndim != 3:
                bands = bands[np.newaxis, ...]
            for band in bands:
                ff.write(band, ii+1)

    if return_raster is True:
        return rio.open(out_path)
