from .gmc import GMC

"""
decorator function to be used inside a class method
creates a new _GMC and adds to global space.
"""
class gmc_connection(object):

    def __init__(self, config=None):
        self.config = config
        #check config

    def __call__(self, fn, *args, **kwargs):
        if not 'gmc' in fn.__globals__:
            fn.__globals__['gmc'] = GMC(self.config)
        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs)
        return wrapper
