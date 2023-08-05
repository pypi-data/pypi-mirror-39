import os
import time
import tempfile



def save_bin_file(data, prefix=None, suffix=None):
    fd, path = tempfile.mkstemp(prefix=prefix, suffix=suffix)
    with os.fdopen(fd, 'wb') as xray:
        xray.write(data)
    return path



def wait_until(condition, interval=0.3, timeout=1, *args, **kwargs):
    """
    wait until condition met or timeout expires
    condtion is an expression that evaluates True or False
    **kwargs are the prams that will be applied to condition
    """
    start = time.time()
    while not condition(**kwargs) and time.time() - start < timeout:
        time.sleep(interval)
