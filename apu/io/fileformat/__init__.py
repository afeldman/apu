from os.path import dirname, basename, isfile, join
from pathlib import Path
import importlib
from inspect import isclass, getmembers
import glob

'''
    supported_formats = {
        ".yml"
        ".json"
        ".jsonl"
        ".pickle"
        ".dill"
        ".h5"
        ".hdf5"
        ".npy"
        ".npz"
'''

__supported_format__ = {}


def supported_format():
    if not bool(__supported_format__):
        modules = glob.glob(join(dirname(__file__), "*.py"))
        module_name = [Path(local_file) for local_file in modules if not '__init__' in local_file]

        # import sensor
        for sensor in module_name:
            mod_gen = importlib.import_module(f"apu.io.fileformat.{sensor.stem}")
            for name, obj in getmembers(mod_gen, isclass):
                __supported_format__[f"{name.lower()}"] = obj

    return __supported_format__
