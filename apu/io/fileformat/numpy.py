from numpy import load, save, savez
from apu.io.fileformat import FileFormat

class NPY(FileFormat):
    def read(self):
        with open(self._filepath.absolute(), mode="br") as numpy_file:
            self.data = load(numpy_file)

    def write(self, sink:str, create:bool=False):
        save(sink, self.data)
        return self.data

class NPZ(NPY):
    def write(self, sink:str, create:bool=False):
        savez(sink, self._args)
        return self.data
