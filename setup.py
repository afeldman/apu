#!/usr/bin/env python3
"""apu: Antons Python Utilities."""

import sys
import platform

# Third party
from setuptools import setup

requires_designpattern = ["dill"]
requires_datetime = ["pytz", "pint", "tzlocal"]
requires = ["GitPython"]
requires_geographie = ["numpy"]
requires_ml = ["torch"]
requires_io = ["h5py", "mat4py", "pyyaml", "dill", "msgpack"]
if not platform.system().lower() == "windows":
    requires_io.append("python_magic")
requires_all = (requires_datetime + requires + requires_geographie +
                requires_designpattern + requires_io + requires_ml)

from apu.__version__ import VERSION

setup(
    version=VERSION,
    package_data={"apu": []},
    project_urls={
        'Documentation': 'https://afeldman.github.io/apu/',
        'Source': 'https://github.com/afeldman/apu',
        'Tracker': 'https://github.com/afeldman/apu/issues',
    },
    install_requires=[
        "dill", "pytz", "pint", "tzlocal", "GitPython", "numpy", "mat4py",
        "semver"
    ],
    extra_requires={
        "all": requires_all,
        "datetime": requires_datetime,
        "setup": requires,
        "geo": requires_geographie,
        "designpattern": requires_designpattern
    },
)