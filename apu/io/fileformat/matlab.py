""" sometime i get matlab mat files """

from mat4py import loadmat, savemat
from apu.io.fileformat import FileFormat

class MAT(FileFormat):
    """ handle mat files """
    def read(self):
        """ read mat file """
        with open(self._filepath.absolute(), mode="br") as mat_file:
            self.data = loadmat(mat_file, meta=False)
        return self.data

    def write(self, sink:str, create:bool=False):
        """ write mat file """
        savemat(sink, self.data)
        return self.data
