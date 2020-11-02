import functools
import threading

class SingletonMixin:

    __lock = threading.Lock()
    __instance = None

    @classmethod
    def instance(cls):
        if cls.__instance is None:
            with cls.__lock:
                # https://en.wikipedia.org/wiki/Double-checked_locking
                if cls.__instance is None:
                    cls.__instance = cls()

        return cls.__instance

def singleton(cls):
    return _singleton(type(f"singleton({cls.__name__})", (cls,), {}))

def meta_singleton(name, bases, attrs):
    return _singleton(type(name,bases,attrs))

def _singleton(new_cls):

    __instance = new_cls()

    def new(clas):
        if isinstance(__instance, clas):
            return __instance
        else:
            raise TypeError(f"can only return {new_cls} instance, \
                              but the user want a {clas} instance")

    new_cls.__new__ = new
    new_cls.__init__ = lambda self: None
    return new_cls

def singleton_dec(cls):

    previous_instances = {}

    @functools.wraps(cls)
    def wrapper(*args, **kwargs):
        if cls in previous_instances and \
           previous_instances.get(cls, None).get('args') == (args, kwargs):
            return previous_instances[cls].get('instance')
        else:
            previous_instances[cls] = {
                'args': (args, kwargs),
                'instance': cls(*args, **kwargs)
            }
            return previous_instances[cls].get('instance')
    return wrapper
