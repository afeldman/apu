from yaml import safe_load, dump
from apu.io.fileformat import FileFormat


class YAML(FileFormat):
    def read(self):
        with open(self._filepath.absolute(), encoding="utf8",
                  mode="r") as yaml_file:
            self.data = safe_load(yaml_file)

    def write(self, sink: str, create: bool = True):
        with open(sink, mode="w", encoding="utf8") as yaml_file:
            dump(self.data,
                 yaml_file,
                 default_flow_style=False,
                 allow_unicode=True)

        return self.data