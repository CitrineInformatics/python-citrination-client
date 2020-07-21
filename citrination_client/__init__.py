import os
import re

from citrination_client.base import *
from citrination_client.search import *
from citrination_client.data import *
from citrination_client.models import *
from citrination_client.views.descriptors import *
from .client import CitrinationClient
from pkg_resources import get_distribution, DistributionNotFound

def __get_version():
    """
    Returns the version of this package, whether running from source or install

    :return: The version of this package
    """
    try:
        # Try local first, if missing setup.py, then use pkg info
        here = os.path.abspath(os.path.dirname(__file__))
        with open(os.path.join(here, "../setup.py")) as fp:
            version_file = fp.read()
            version_match = re.search(r"version=['\"]([^'\"]*)['\"]",
                                      version_file, re.M)
            if version_match:
                return version_match.group(1)
    except IOError:
        pass

    try:
        _dist = get_distribution('citrination_client')
        # Normalize case for Windows systems
        # Using realpath in case directories are symbolic links
        dist_loc = os.path.realpath(os.path.normcase(_dist.location))
        here = os.path.realpath(os.path.normcase(__file__))
        if not here.startswith(os.path.join(dist_loc, 'citrination_client')):
            # not installed, but there is another version that *is*
            raise DistributionNotFound
    except DistributionNotFound:
        raise RuntimeError("Unable to find version string.")
    else:
        return _dist.version

__version__ = __get_version()
