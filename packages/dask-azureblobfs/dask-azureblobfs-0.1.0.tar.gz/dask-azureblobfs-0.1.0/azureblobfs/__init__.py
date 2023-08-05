# -*- coding: utf-8 -*-

"""Top-level package for Dask Azure Blob FileSystem."""

from pkg_resources import get_distribution, DistributionNotFound


__author__ = """Manish Sinha"""
__email__ = 'masinha@microsoft.com'
__name__ = "dask-azureblobfs"

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound as dex:
    # package is not installed
    print("Package {name} is not installed. Exception raise:\n{exp}".format(name=__name__, exp=dex))
    from setuptools_scm import get_version
    import os
    __version__ = get_version(
        os.path.dirname(os.path.dirname(__file__))
    )
