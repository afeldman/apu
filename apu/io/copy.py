import os
import shutil
from multiprocessing import Pool, Lock
lock = Lock()

from pathlib import Path
from tqdm import tqdm

from apu.mp.parallel_for import parallel_for
from apu.io.fileformat import compair

def copy_(file_):
    src_file = file_[0]
    dst_file = file_[1]

    with lock:
        print(f"{src_file} -> {dst_file}")

    shutil.copy(src_file, dst_file)

class Copy:
    def __init__(self, origin:str, dest:str, number:int=None, sort:bool=True, verbose:bool = False):
        self.origin = Path(origin)
        self.destination = Path(dest)
        self.pool = Pool(os.cpu_count())
        self.verbose = verbose
        self.count = 1 if number is None or number <= 0 else number

        self.files = self.__files(sort=sort)

    def __files(self, sort):
        files_ = set()
        for src_dir, _, files in os.walk(self.origin):

            dst_dir = Path(src_dir.replace(str(self.origin), str(self.destination), 1))
      
            if not dst_dir.exists():
                if self.verbose:
                    print(f"{dst_dir} not exists")
                dst_dir.mkdir(parents=True, exist_ok=True)

            if sort:
                file_list = sorted(files[:self.count] if len(files) >= self.count else files,
                               key=lambda path: path)
            else:
                file_list = files

            if len(file_list) == 0:
                print(f"{src_dir} is empty?")
                continue
            else:
                for file_ in file_list:
                    src_file = Path(src_dir) / file_
                    dst_file = dst_dir / file_

                    if dst_file.exists() and not compair(src_file, dst_file, method="md5"):
                        print(f"{src_file} already copied")
                    else:
                        files_.add(tuple( (src_file, dst_file)))
        return files_


    def __call__(self, parallel:bool=False):
        if self.files is None or len(self.files) == 0:
            return

        if parallel:
            parallel_for(copy_, self.files)
        else:
            for file_ in tqdm(self.files):
                copy_(file_)
