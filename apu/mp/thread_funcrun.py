import threading
import functools

def thread_funcrun(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        threading.Thread(target=func, args=(args, kwargs)).start()
        print(f"Thread started for function {func}")
    return wrapper

def thread_n_funcrun(number_of_threads=1):
    def wrapper(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(number_of_threads):
                threading.Thread(target=func, args=(args, kwargs)).start()
                print(f"Thread started for function {func}")
        return wrapper
    return wrapper