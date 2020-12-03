#https://github.com/lebedov/msgpack-numpy

from functools import partial

from apu.encoding.bytes import NumpyBytes

import msgpack
from msgpack import Packer as _Packer, Unpacker as _Unpacker, unpack as _unpack, unpackb as _unpackb

if msgpack.version < (1, 0, 0):
    print(f"do not support msgpack version {msgpack.version}")

    class Packer(_Packer):
        pass

    class Unpacker(_Unpacker):
        pass
else:

    class Packer(_Packer):
        def __init__(self,
                     default=None,
                     use_single_float=False,
                     autoreset=True,
                     use_bin_type=True,
                     strict_types=False,
                     datetime=False,
                     unicode_errors=None):
            default = partial(NumpyBytes.encode, chain=default)
            super().__init__(default=default,
                             use_single_float=use_single_float,
                             autoreset=autoreset,
                             use_bin_type=use_bin_type,
                             strict_types=strict_types,
                             datetime=datetime,
                             unicode_errors=unicode_errors)

    class Unpacker(_Unpacker):
        def __init__(self,
                     file_like=None,
                     read_size=0,
                     use_list=True,
                     raw=False,
                     timestamp=0,
                     strict_map_key=True,
                     object_hook=None,
                     object_pairs_hook=None,
                     list_hook=None,
                     unicode_errors=None,
                     max_buffer_size=100 * 1024 * 1024,
                     ext_hook=msgpack.ExtType,
                     max_str_len=-1,
                     max_bin_len=-1,
                     max_array_len=-1,
                     max_map_len=-1,
                     max_ext_len=-1):
            object_hook = partial(NumpyBytes.decode, chain=object_hook)
            super().__init__(file_like=file_like,
                             read_size=read_size,
                             use_list=use_list,
                             raw=raw,
                             timestamp=timestamp,
                             strict_map_key=strict_map_key,
                             object_hook=object_hook,
                             object_pairs_hook=object_pairs_hook,
                             list_hook=list_hook,
                             unicode_errors=unicode_errors,
                             max_buffer_size=max_buffer_size,
                             ext_hook=ext_hook,
                             max_str_len=max_str_len,
                             max_bin_len=max_bin_len,
                             max_array_len=max_array_len,
                             max_map_len=max_map_len,
                             max_ext_len=max_ext_len)


def pack(o, stream, **kwargs):
    packer = Packer(**kwargs)
    stream.write(packer.pack(o))


def packb(o, **kwargs):
    return Packer(**kwargs).pack(o)


def unpack(stream, **kwargs):
    object_hook = kwargs.get('object_hook')
    kwargs['object_hook'] = partial(NumpyBytes.decode, chain=object_hook)
    return _unpack(stream, **kwargs)


def unpackb(packed, **kwargs):
    object_hook = kwargs.get('object_hook')
    kwargs['object_hook'] = partial(NumpyBytes.decode, chain=object_hook)
    return _unpackb(packed, **kwargs)


load = unpack
loads = unpackb
dump = pack
dumps = packb


def patch():
    """
    Monkey patch msgpack module to enable support for serializing numpy types.
    """

    setattr(msgpack, 'Packer', Packer)
    setattr(msgpack, 'Unpacker', Unpacker)
    setattr(msgpack, 'load', unpack)
    setattr(msgpack, 'loads', unpackb)
    setattr(msgpack, 'dump', pack)
    setattr(msgpack, 'dumps', packb)
    setattr(msgpack, 'pack', pack)
    setattr(msgpack, 'packb', packb)
    setattr(msgpack, 'unpack', unpack)
    setattr(msgpack, 'unpackb', unpackb)


class NumpyMSG:
    def __init__(self):
        patch()

    @staticmethod
    def start():
        return NumpyMSG()

    @staticmethod
    def encode(self, msg):
        return msgpack.packb(msg)

    @staticmethod
    def decode(self, coded_msg, use_list=True, max_bin_len=-1):
        return msgpack.unpackb(coded_msg,
                               use_list=use_list,
                               max_bin_len=max_bin_len)
