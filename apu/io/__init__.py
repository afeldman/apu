""" apu.io anton python utils input output module """

__version__ = (0, 0, 1)
__email__ = "anton.feldmann@gmail.com"
__author__ = "anton feldmann"

from apu.io.dill import reconstruct, load

__all__ = ['reconstruct', "load"]

import os
from typing import Optional


def download(source: str, sink: Optional[str] = None) -> str:
    # Core Library
    from urllib.request import urlretrieve

    if sink is None:
        sink = os.path.abspath(os.path.split(source)[1])
    urlretrieve(source, sink)
    return sink

def urlread(url: str, encoding: str = "utf8") -> str:
    # Core Library
    from urllib.request import urlopen

    response = urlopen(url)
    content = response.read()
    content = content.decode(encoding)
    return content
