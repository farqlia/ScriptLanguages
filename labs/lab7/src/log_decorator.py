import logging
import datetime
import typing
import time


def log(level):

    logging_format = '%(levelname)s: %(asctime)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=logging_format)
    logger = logging.getLogger()

    def decorator(obj):

        def wrapper(*args, **kwargs):

            start = time.perf_counter()
            msg = f"Starting at {datetime.datetime.now()}"
            msg += ("\nCreating instance of a class %s\nCreated %s\n" if obj.__class__
                    == type else f"\nInvoking function %s\nComputed %s\n")

            result = obj(*args, **kwargs)

            measured_time = time.perf_counter() - start
            msg += "Invocation took %.6f seconds"
            logger.log(level=level, msg=msg % (obj.__name__, result, measured_time))
            return result

        return wrapper

    return decorator


@log(logging.DEBUG)
def some_function():
    pass


if __name__ == "__main__":
    some_function()
