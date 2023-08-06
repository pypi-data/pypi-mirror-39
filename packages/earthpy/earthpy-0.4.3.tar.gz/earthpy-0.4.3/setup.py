import os
import setuptools
from numpy.distutils.core import setup


DISTNAME = "earthpy"
DESCRIPTION = "A set of helper functions to make working with spatial data in open source tools easier. This package is maintained by Earth Lab and was originally designed to support the earth analytics education program."
MAINTAINER = "Leah Wasser"
MAINTAINER_EMAIL = "leah.wasser@colorado.edu"
VERSION = "0.4.03"


def configuration(parent_package="", top_path=None):
    if os.path.exists("MANIFEST"):
        os.remove("MANIFEST")

    from numpy.distutils.misc_util import Configuration

    config = Configuration(None, parent_package, top_path)
    config.add_subpackage("earthpy")

    return config

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()


if __name__ == "__main__":
    setup(
        configuration=configuration,
        name=DISTNAME,
        maintainer=MAINTAINER,
        include_package_data=True,
        maintainer_email=MAINTAINER_EMAIL,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type='text/markdown',
        version=VERSION,
        install_requires=[
            "tqdm",
            "pandas",
            "numpy",
            "geopandas",
            "matplotlib",
            "rasterio",
            "download",
        ],
        zip_safe=False,  # the package can run out of an .egg file
        classifiers=[
            "Intended Audience :: Developers",
            "License :: OSI Approved :: BSD License",
            "Programming Language :: Python",
            "Topic :: Software Development",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX",
            "Operating System :: Unix",
            "Operating System :: MacOS",
        ],
        package_data={DISTNAME: [
            "example-data/*.json",
            "example-data/*.tif",
            "example-data/*.geojson",
            "example-data/*.shp",
            "example-data/*.shx",
            "example-data/*.prj",
            "example-data/*.dbf"
        ]},
    )
