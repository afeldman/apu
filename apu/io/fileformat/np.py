""" read numpy files """
from numpy import load, save, savez
from apu.io.fileformat import FileFormat

class NPY(FileFormat):
    """ handle npy files """
    def read(self):
        """ read npy files """
        with open(self._filepath.absolute(), mode="br") as numpy_file:
            self.data = load(numpy_file)
        return self.data

    def write(self, sink:str, create:bool=False):
        """ write npy files """
        save(sink, self.data)
        return self.data

class NPZ(NPY):
    """ handle npz files"""
    def write(self, sink:str, create:bool=False):
        """ write npz files """
        savez(sink, self._args)
        return self.data
