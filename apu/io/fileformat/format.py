from typing import Dict, Any

import tzlocal
from datetime import datetime

from abc import ABC, abstractmethod
from pathlib import Path

from apu.io.hash import DIGITS

class FileFormat(ABC):
    def __init__(self, path: str, kwargs: Dict = dict()):
        self._filepath = Path(path)
        self._args = kwargs
        self.data = None

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def write(self, sink:str, create: bool = True):
        pass

    def __exists(self, create: bool = False):
        if self._filepath.exists():
            return True
        else:
            if create:
                self._filepath.touch("755", exist_ok=True)
                return True
            else:
                raise FileNotFoundError(f"cannot find {self._filepath}")
            return False

    @property
    def creation_time(self):
        tz = tzlocal.get_localzone()
        #not tested on windows
        return datetime.fromtimestamp(
            self._filepath.lstat().st_ctime).replace(tzinfo=tz)

    @property
    def modification_time(self):
        tz = tzlocal.get_localzone()
        return datetime.fromtimestamp(
            self._filepath.lstat().st_mtime).replace(tzinfo=tz)

    @property
    def access_time(self):
        tz = tzlocal.get_localzone()
        return datetime.fromtimestamp(
            self._filepath.lstat().st_atime).replace(tzinfo=tz)

    def meta(self) -> Any:
        meta: Dict[str, Any] = {
            "filepath": self._filepath.absolute(),
            "creation_data": self.creation_time,
            "modification_time": self.modification_time,
            "access_time": self.access_time
        }

        try:
            import magic

            f_mime = magic.Magic(mime=True, uncompress=True)
            f_other = magic.Magic(mime=False, uncompress=True)
            meta["mime"] = f_mime.from_file(meta["filepath"])
            meta["magic-type"] = f_other.from_file(meta["filepath"])
        except ImportError:
            pass

        return meta

    def fingerprint(self, method:str="sha1"):
        method = method.lower()
        assert (method in DIGITS.keys()
            ), f"cannot find the hashmethod. please select on of {DIGITS.keys()}"
        assert (self.__exists(create=False)), f"{self._filepath} is not a file!"

        # retrun hashed file
        return DIGITS[method](self._filepath)

    def compair(self, filepath:str, method="sha1"):
        return str(self.fingerprint(method=method).hexdigest()) == str(FileFormat(filepath).fingerprint(method=method))
