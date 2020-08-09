#!/usr/bin/env python

"""apu: Antons Python Utilities."""

# Third party
from setuptools import setup

requires_datetime = ["pytz"]
requires_setup = ["GitPython"]
requires_all = (
    + requires_time
    + requires_setup
)

setup(
    package_data={"apu": []},
    extras_require={
        "all": requires_all,
        "datetime": requires_time,
        "setup": requires_setup,
    },
)