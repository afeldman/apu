import functools

def time_it(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        from time import time
        start_time = time()
        func(*args, **kwargs)
        end_time = time()
        print(f"Time taken by the function is [{end_time-start_time}] sec")
    return wrapper
