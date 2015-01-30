""" Provides a basic interface based on concurrent futures to be shared globally
between PyXLL modules.

TODO: integrate it with the async_fun machinerie of pyxll to support proper COM
marshalling if needed.

"""
import futures

_executor = None

def get_executor(n=2):
    global _executor
    if _executor is None:
        _executor = futures.ThreadPoolExecutor(max_workers=n)
    return _executor

