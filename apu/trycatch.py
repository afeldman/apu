import functools

def tryexcept(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as excep:
            print(f"Exception occurred: [{excep}]")
    return wrapper
