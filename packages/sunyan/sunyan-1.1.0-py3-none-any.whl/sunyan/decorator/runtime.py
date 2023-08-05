import time
import logging
from functools import wraps

logging.basicConfig(level=logging.INFO)

def runtime(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        used = time.time()-start
        msg = '%s used time: %0.3f' %(func.__name__,used)
        logging.info(msg)
        return res
    return wrap