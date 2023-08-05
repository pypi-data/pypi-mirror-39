from inspect import signature
from functools import update_wrapper

def typeassert(*ty_args,**ty_kargs):
    def decorator(func):
        sig = signature(func)
        btypes =  sig.bind_partial(*ty_args,**ty_kargs).arguments
        def wrap(*args,**kwargs):
            for name,obj in sig.bind(*args,**kwargs).arguments.items():
                if name in btypes:
                    if not isinstance(obj,btypes[name]):
                        raise  TypeError('"%s" must be "%s"' %(name,btypes[name]))
            return func(*args,**kwargs)
        update_wrapper(wrap, func)
        return wrap
    return decorator