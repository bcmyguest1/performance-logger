import logging
import sys
import time
from functools import wraps


class PerformanceLogger:
    def __init__(self, level: int = logging.INFO, print_ret: bool = False):
        self.level: int = level
        self.print_ret: bool = print_ret
        self.float_format: str = ".3f"

    def perf_log(self):

        def log_time_decorator(func):
            @wraps(func)
            def wrapper(*args, logger=None, print_ret=None, level=None, **kwargs):

                if logger is None:
                    logger = logging.getLogger(sys.modules[func.__module__].__name__)
                if level is None:
                    level = self.level
                if print_ret is None:
                    print_ret = self.print_ret
                logger.level = self.level

                start = time.process_time()
                res = None
                try:
                    res = func(*args, **kwargs)
                except Exception as e:
                    logger.msg(f"{str(e.__traceback__)}")
                end = time.process_time()
                logger.log(level,
                           f"Ran in: {f'{{:{self.float_format}}}'.format(end - start)}s. "
                           f"Result: {str(res) if print_ret else '<NULL>'}")

            return wrapper

        return log_time_decorator


_inst = PerformanceLogger()
log_time = _inst.perf_log

if __name__ == "__main__":
    # basic usage
    import uuid
    import logging

    # Log format
    _format = logging.Formatter(
        '%(asctime)s %(levelname)s %(name)s.%(funcName)s : %(message)s',
        '%Y-%m-%d %H:%M:%S')

    def init():
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(_format)
        logger.addHandler(stream_handler)


    level = logging.INFO
    init()


    @log_time()
    def func(test, n=1_000_000):
        for _ in range(n):
            test = test ** 2


    func(1)
