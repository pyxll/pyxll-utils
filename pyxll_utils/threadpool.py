import futures

_executor = None

def get_executor(n=2):
    global _executor
    if _executor is None:
        _executor = futures.ThreadPoolExecutor(max_workers=n)
    return _executor
