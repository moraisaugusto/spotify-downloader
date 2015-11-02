def retry(tries, delay=1, backoff=2):
    """
    A retry decorator with exponential backoff,
    Retries a function or method if Exception occurred
 
    Args:
        tries: number of times to retry, set to 0 to disable retry
        delay: initial delay in seconds(can be float, eg 0.01 as 10ms),
            if the first run failed, it would sleep 'delay' second and try again
        backoff: must be greater than 1, 
            further failure would sleep delay *= backoff second 
    """
    import time
    import math
 
    if backoff <= 1:
        raise ValueError("backoff must be greater than 1")
 
    tries = math.floor(tries)
    if tries < 0:
        raise ValueError("tries must be 0 or greater")
 
    if delay <= 0:
        raise ValueError("delay must be greater than 0")
 
    def decorator(func):
        def wrapper(*args, **kwargs):
            _tries, _delay = tries, delay
            _tries += 1 #ensure we call func at least once
            while _tries > 0:
                try:
                    ret = func(*args, **kwargs)
                    return ret
                except Exception as e:
                    _tries -= 1
                    #retried enough and still fail? raise orignal exception
                    if _tries == 0: raise
                    time.sleep(_delay)
                    #wait longer after each failure
                    _delay *= backoff
        return wrapper
 
    return decorator

'''

import time
from functools import wraps


def retry(ExceptionToCheck, tries=4, delay=3, backoff=2, logger=None):
    """Retry calling the decorated function using an exponential backoff.

    http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    original from: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry

    :param ExceptionToCheck: the exception to check. may be a tuple of
        exceptions to check
    :type ExceptionToCheck: Exception or tuple
    :param tries: number of times to try (not retry) before giving up
    :type tries: int
    :param delay: initial delay between retries in seconds
    :type delay: int
    :param backoff: backoff multiplier e.g. value of 2 will double the delay
        each retry
    :type backoff: int
    :param logger: logger to use. If None, print
    :type logger: logging.Logger instance
    """
    def deco_retry(f):

        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except (ExceptionToCheck, e):
                    msg = "%s, Retrying in %d seconds..." % (str(e), mdelay)
                    if logger:
                        logger.warning(msg)
                    else:
                        print (msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry
'''