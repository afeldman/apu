import numpy as np

from json.encoder import JSONEncoder
from json.decoder import JSONDecoder

class NumpyEncoder(JSONEncoder):
    """ Custom encoder for numpy data types """

    def np_list(self, obj):
        return obj.tolist()

    def np_float(self, obj):
        return float(obj)

    def np_int(self, obj):
        return int(obj)

    def np_complex(self, obj):
        return { "real": obj.real, "imag": obj.imag }

    def np_bool(self, obj):
        return bool(obj)

    def np_null(self, obj):
        return None

    def np(self, obj):
        if isinstance(obj, np.integer):

            return self.np_int(obj)

        elif isinstance(obj, np.floating):
            return self.np_float(obj)

        elif isinstance(obj, (np.complex_, np.complex64, np.complex128)):
            return self.np_complex(obj)

        elif isinstance(obj, (np.ndarray,)):
            return self.np_list(obj)

        elif isinstance(obj, (np.bool_)):
            return self.np_bool(obj)

        elif isinstance(obj, (np.void)):
            return self.np_null(obj)

        return JSONEncoder.default(self, obj)

    def default(self, obj):

        return self.np(obj)

class NumpyDecoder(JSONDecoder):
    """ Custom decode for numpy data types """

    _recursable_types = [str, list, dict]

    def _is_recursive(self, obj):
        return type(obj) in NumpyDecoder._recursable_types

    def decode(self, obj, *args, **kwargs):
        if not kwargs.get('recurse', False):
            obj = super().decode(obj, *args, **kwargs)

        if isinstance(obj, list):
            try:
                return np.array(obj)
            except:
                for item in obj:
                    if self._is_recursive(item):
                        obj[item] = self.decode(item, recurse=True)

        elif isinstance(obj, dict):
            for key, value in obj.items():
                if str(key) in "real":
                    return np.complex(obj['real'], obj['imag'])
                elif self._is_recursive(value):
                    obj[key] = self.decode(value, recurse=True)

        elif isinstance(obj, bool):
            return np.bool(obj)

        elif isinstance(obj, float):
            return np.float(obj)

        elif obj is None:
            return np.void

        else:
            return obj
