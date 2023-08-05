import wasabi as wb
from functools import wraps


def loading(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        msg = wb.Printer()
        with msg.loading('Loading:'):
            res = func(*args, **kwargs)
        msg.good("Successfully loaded!")
        return res
    return wrap

import time
from tqdm import tqdm

@loading
def loaddata():
    for i in tqdm(range(3)):
        time.sleep(1)

if __name__ == '__main__':
    loaddata()