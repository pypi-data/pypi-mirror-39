import time

def timed(function):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        ret = function(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{elapsed} seconds for method: {function.__name__}")
        return ret
    return wrapper

def turn_timer(function, turn):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        ret = function(*args, **kwargs)
        elapsed = time.perf_counter() - start
        # turn, method, elapsed seconds
        print(f"timer,{turn},{function.__name__},{elapsed}")
        return ret
    return wrapper