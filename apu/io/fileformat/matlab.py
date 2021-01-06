from mat4py import loadmat, savemat
from apu.io.fileformat import FileFormat

class MAT(FileFormat):
    def read(self):
        with open(self._filepath.absolute(), mode="br") as mat_file:
            self.data = loadmat(mat_file, meta=False)

    def write(self, sink:str, create:bool=False):
        savemat(sink, self.data)
        return self.data