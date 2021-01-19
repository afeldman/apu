""" apu.io anton python utils input output module """

__version__ = (0, 0, 1)
__email__ = "anton.feldmann@gmail.com"
__author__ = "anton feldmann"

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
from apu.io.__fileformat import supported_format

def read(filepath: str, **kwargs: Any) -> Any:

    supported_formats = supported_format

    filepathl = filepath.lower()

    if filepathl.endswith(".csv"):
        csv = CSV( path=filepath, kwargs=kwargs )
        return csv.read()
    elif filepathl.endswith(".dill"):
        dill = DILL(path=filepath, kwargs=kwargs)
        return dill.read()
    elif  filepathl.endswith(".json"):
        json = JSON(path=filepath, kwargs=kwargs)
        return json.read()
    elif filepathl.endswith(".jsonl"):
        jsonl = JSONL(path=filepath, kwargs=kwargs)
        return jsonl.read()
    elif filepathl.endswith(".mat"):
        mat = MAT(path=filepath, kwargs=kwargs)
        return mat.read()
    elif filepathl.endswith('.npy'):
        npy = NPY(path=filepath, kwargs=kwargs)
        return npy.read()
    elif filepathl.endswith('.npz'):
        npz = NPZ(path=filepath, kwargs=kwargs)
        return npz.read()
    elif filepathl.endswith(".pickle"):
        pickle = PICKLE(path=filepath, kwargs=kwargs)
        return pickle.read()
    elif filepathl.endswith(".yml") or filepathl.endswith(".yaml"):
        yaml = YAML(path=filepath, kwargs=kwargs)
        return yaml.read()
    elif filepathl.endswith(".h5") or filepathl.endswith(".hdf5"):
        raise NotImplementedError(
            "HDF5 is not supported. See "
            "https://stackoverflow.com/a/41586571/562769"
            " as a guide how to use it."
        )
    else:
        raise NotImplementedError(
            f"File '{filepath}' does not end with one "
            f"of the supported file name extensions. "
            f"Supported are: {supported_formats}"
        )
