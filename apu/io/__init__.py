""" apu.io anton python utils input output module """

__version__ = (0, 0, 1)
__email__ = "anton.feldmann@gmail.com"
__author__ = "anton feldmann"

from pathlib import Path

from apu.io.dill import reconstruct, load

__all__ = ['reconstruct', "load"]

from typing import Any
from apu.io.__fileformat.csv import CSV
from apu.io.__fileformat.dill import DILL
from apu.io.__fileformat.json import (JSON, JSONL)
from apu.io.__fileformat.matlab import MAT
from apu.io.__fileformat.np import (NPY, NPZ)
from apu.io.__fileformat.pickel import PICKLE
from apu.io.__fileformat.yaml import YAML
from apu.io.__fileformat.h5 import H5
from apu.io.__fileformat import supported_format

def read(filepath: str, **kwargs: Any) -> Any:

    supported_formats = supported_format()

    filedatapath = Path(filepath).suffix
    filedata = None

    for suffix, fileformat in supported_format().items():
        if filedatapath  in suffix:
            filedata = fileformat(path=filepath, kwargs=kwargs)
            break

    if filedata is not None:
        return filedata.read() 
    else:
        raise NotImplementedError(
            f"File '{filepath}' does not end with one "
            f"of the supported file name extensions. "
            f"Supported are: {supported_formats.keys()}"
        )

def write(filepath: str, data: Any, **kwargs: Any) -> Any:

    supported_formats = supported_format()

    filepathl = Path(filepath)

    filedata = supported_formats.get(filepathl.suffix, None)
    if filedata is not None:
        filedata = filedata(path=filepathl, kwargs=kwargs, data=data)
        return filedata.write()
    else:
        raise NotImplementedError(
            f"File '{filepath}' does not end with one "
            f"of the supported file name extensions. "
            f"Supported are: {supported_formats.keys()}"
        )
