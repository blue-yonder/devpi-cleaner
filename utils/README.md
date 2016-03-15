Find Heavy Packages on Devpi
============================

The [`find_heavy_packages.py` script](find_heavy_packages.py) finds those packages and indices on your Devpi installation that use up the most space.

Usage
-----

    usage: find_heavy_packages.py [-h] [-v] [--only-dev] devpi_directory
    
    Find heavy packages on Devpi
    
    positional arguments:
      devpi_directory  The data directory of the Devpi server to inspect.
    
    optional arguments:
      -h, --help       show this help message and exit
      -v, --verbose    Show debug information.
      --only-dev       Find only development versions as specified by PEP440.

Tested Devpi Versions
---------------------

This script has been tested on data directories of the following Devpi versions:

* devpi-server 2.5.3
