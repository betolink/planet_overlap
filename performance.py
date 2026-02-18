import time
import logging
import tracemalloc
from functools import wraps


def track_performance(func):
    """
    Decorator to track runtime and memory usage of functions.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):

        logging.info(f"Starting: {func.__name__}")

        # Start timing
        start_time = time.time()

        # Start memory tracking
        tracemalloc.start()

        result = func(*args, **kwargs)

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        elapsed = time.time() - start_time

        logging.info(
            f"Completed: {func.__name__} | "
            f"Runtime: {elapsed:.2f}s | "
            f"Peak Memory: {peak / 10**6:.2f} MB"
        )

        return result

    return wrapper
