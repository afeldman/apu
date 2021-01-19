""" apu.io anton python utils input output module """

__version__ = (0, 0, 1)
__email__ = "anton.feldmann@gmail.com"
__author__ = "anton feldmann"

from apu.io.dill import reconstruct, load

__all__ = ['reconstruct', "load"]

from typing import Any
from apu.io.fileformat.csv import CSV
from apu.io.fileformat.dill import DILL
from apu.io.fileformat.json import (JSON, JSONL)
from apu.io.fileformat.matlab import MAT
from apu.io.fileformat.np import (NPY, NPZ)
from apu.io.fileformat.pickel import Pickle
from apu.io.fileformat.yaml import YAML

def read(filepath: str, **kwargs: Any) -> Any:

    supported_formats = (".csv", ".dill", ".json", ".jsonl", ".mat", ".npy", ".npz", ".pickle", ".yml", ".yaml")

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
        pickle = Pickle(path=filepath, kwargs=kwargs)
        return pickle.read()
    elif filepathl.endswith(".yml") or filepathl.endswith(".yaml"):
        yaml = YAML(path=filepath, kwargs=kwargs)
        return yaml.read()
    elif filepath.lower().endswith(".h5") or filepath.lower().endswith(".hdf5"):
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