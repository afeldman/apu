""" handling H5 files """
from typing import Dict, Any

import h5py

from apu.io.fileformat import FileFormat

class HDF5(FileFormat):
    """ h5 file handling realization """
    def __init__(self, path: str, kwargs: Dict = dict) -> None:
        super().__init__(path, kwargs)
        self.h5_file = h5py.File(self._filepath.absolute(), mode="r")

    def keys(self):
        """ get all keys """
        return self.h5_file.keys()

    def has_key(self, key) -> bool:
        """ is the key in the file """
        return key in list(self.keys())

    def __getitem__(self, key) -> Any:
        """ get item from dataset"""
        if self.has_key(key):
            return self.h5_file[key]
        return None

    def __setitem__(self, key, value) -> None:
        """ set value to dataset """
        self.h5_file[key] = value

    def __del__(self):
        """ close by darbage collector """
        self.h5_file.close()

    def read(self, keys = None):
        """ read file or only a special datasection """
        ret = list()
        if keys is None:
            key = list(self.keys())[0]
            ret.append(list(self.h5_file[key]))
        else:
            if isinstance(keys, list):
                for key in keys:
                    ret.append(list(self.h5_file[key]))
            else:
                ret.append(self.h5_file[keys])
        return ret

    def write(self, sink:str, create:bool=False):
        """ write to h5 file
        TODO: implementation
        """
        #with h5py.File(sink, "w") as h5_file:
        #    pass
