""" reading and writing yaml files """

#from h5py import h5_load
from apu.io.fileformat import FileFormat

class H5(FileFormat):
    """ reading and writing yaml files"""
    def read(self):
        return self.data

    def write(self, sink: str, create: bool = True):
        return self.data
