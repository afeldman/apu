import numpy as np

class Bytes(bytes):
    @staticmethod
    def b2s(x: bytes) -> str:
        if isinstance(x, bytes):
            return x.decode()
        else:
            return str(x)

class NumpyBytes(Bytes):
    @staticmethod
    def array2byte(matrix: np.ndarray) -> bytes:
        if not isinstance(matrix, np.ndarray):
            raise TypeError(f"argument not numpy array type")
        return matrix.data if matrix.flags['C_CONTIGUOUS'] else matrix.tobytes(
        )

    @staticmethod
    def n2b(num) -> bytes:
        return num.data

    @staticmethod
    def encode(npobj, chain=None):
        if isinstance(npobj, np.ndarray):
            if npobj.dtype.kind == 'V':
                kind = b'V'
                descr = npobj.dtype.descr
            else:
                kind = b''
                descr = npobj.dtype.str
            return {
                b'nd': True,
                b'type': descr,
                b'kind': kind,
                b'shape': npobj.shape,
                b'data': NumpyBytes.array2byte(npobj)
            }

        elif isinstance(npobj, (np.bool_, np.number)):
            return {
                b'nd': False,
                b'type': npobj.dtype.str,
                b'data': NumpyBytes.n2b(npobj)
            }

        elif isinstance(npobj, complex):
            return {b'complex': True, b'data': npobj.__repr__()}
        else:
            return npobj if chain is None else chain(npobj)

    @staticmethod
    def decode(npobj, chain=None):
        try:
            if b'nd' in npobj:
                if npobj[b'nd'] is True:
                    if b'kind' in npobj and npobj[b'kind'] == b'V':
                        descr = [tuple(NumpyBytes.b2s(t) if type(t) is bytes else t for t in d) \
                             for d in npobj[b'type']]
                    else:
                        descr = npobj[b'type']
                    return np.frombuffer(
                        npobj[b'data'],
                        dtype=NumpyBytes._unpack_dtype(descr)).reshape(
                            npobj[b'shape'])
                else:
                    descr = npobj[b'type']
                    return np.frombuffer(npobj[b'data'],
                                         dtype=NumpyBytes._unpack_dtype(descr))[0]
            elif b'complex' in npobj:
                return complex(NumpyBytes.b2s(npobj[b'data']))
            else:
                return npobj if chain is None else chain(npobj)
        except KeyError:
            return npobj if chain is None else chain(npobj)

    @staticmethod
    def _unpack_dtype(dtype):
        if isinstance(dtype, (list, tuple)):
            # Unpack structured dtypes of the form: (name, type, *shape)
            dtype = [
                (subdtype[0], NumpyBytes._unpack_dtype(subdtype[1])) + tuple(subdtype[2:])
                for subdtype in dtype
            ]
        return np.dtype(dtype)
