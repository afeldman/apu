from typing import Dict, Any

import h5py

from apu.io.fileformat import FileFormat

class HDF5(FileFormat):
    def __init__(self, path: str, kwargs: Dict = dict()) -> None:
        super().__init__(path, kwargs)
        self.h5_file = h5py.File(self._filepath.absolute(), mode="r")

    def keys(self):
        return self.h5_file.keys()

    def _key_(self, key) -> bool:
        return key in list(self.keys())

    def __getitem__(self, key) -> Any:
        if self._key_(key):
            return self.h5_file[key]

    def __setitem__(self, key, value) -> None:
        self.h5_file[key] = value

    def __del__(self):
       self.h5_file.close()

    def read(self, keys = None):
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
        with h5py.File(sink, "w") as h5_file:
            pass
