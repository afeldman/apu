from pickle import dump, load, HIGHEST_PROTOCOL
from apu.io.fileformat import FileFormat

class Pickle(FileFormat):
    def read(self):
        with open(self._filepath.absolute(), mode="br") as pickle_file:
            self.data = load(pickle_file)

    def write(self, sink:str, create:bool=False):
        if "protocol" not in self._args:
            self._args["protocol"] = HIGHEST_PROTOCOL
        with open(sink, "wb") as handle:
            dump(self.data, handle, **self._args)
        return self.data
