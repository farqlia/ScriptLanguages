import logging
import datetime
import typing


def log(level):
    logging_format = '%(levelname)s: %(asctime)s - %(message)s'
    logging.basicConfig(level=level, format=logging_format)
    logger = logging.getLogger()

    def decorator(obj):

        def wrapper(*args, **kwargs):

            start_time = datetime.datetime.now()
            logger.log(level=level, msg=f"Starting at {start_time}")

            msg = "Creating instance of a class %s" if obj.__class__ == type else f"Invoking function %s"
            logger.log(level, msg, obj.__name__)

            result = obj(*args, **kwargs)

            msg = "Created %s" if obj.__class__ == type else f"Computed %s"

            logger.log(level, msg, result)

            end_time = datetime.datetime.now()
            time = (end_time - start_time).total_seconds()

            logger.log(level=level, msg=f"Invocation took {time} seconds")

            return result
        return wrapper

    return decorator


