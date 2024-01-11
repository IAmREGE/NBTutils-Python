import logging
import sys
from setuptools import find_packages, setup

if sys.version_info < (3, 8) :
    raise SystemError("Python 3.8 or later required")
elif sys.version_info > (3, 13) :
    logging.warning("Not tested on later version of Python 3.13.")

setup(
    name = "nbtutils",
    version = "0.0.1a1",
    author = "REGE",
    packages = find_packages()
)