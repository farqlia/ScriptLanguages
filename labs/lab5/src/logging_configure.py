import logging
import sys
import labs.lab5.src.regex_ssh_utilis as analyze_ssh_logs

OPERATIONS = {
    analyze_ssh_logs.MessageType.SUCCESSFUL_LOGIN: logging.info,
    analyze_ssh_logs.MessageType.CLOSED_CONNECTION: logging.info,
    analyze_ssh_logs.MessageType.UNSUCCESSFUL_LOGIN: logging.warning,
    analyze_ssh_logs.MessageType.INCORRECT_USERNAME: logging.error,
    analyze_ssh_logs.MessageType.INCORRECT_PASSWORD: logging.error,
    analyze_ssh_logs.MessageType.BREAK_IN_ATTEMPT: logging.critical
}


def configure_logging(minimal_level=logging.DEBUG):
    logging_format = '%(levelname)s: %(asctime)s - %(message)s'
    formatter = logging.Formatter(logging_format)
    error_handler = logging.StreamHandler(sys.stderr)
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)

    console_handler.addFilter(filter_maker(logging.WARNING))
    console_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(minimal_level)
    logger.addHandler(console_handler)
    logger.addHandler(error_handler)


def filter_maker(level):

    def filter_log(record):
        return record.levelno <= level

    return filter_log


def compute_bytes(log_entry):
    return sum(sys.getsizeof(elem) for elem in log_entry)


def log_bytes_read(log_entry):
    logging.debug(f"Bytes read: {compute_bytes(log_entry)}")

def log_data(log_entry, display=False):

    mssg_type = analyze_ssh_logs.get_message_type(log_entry)

    log_bytes_read(log_entry)

    value = mssg_type.format()
    if display:
        value += f", '{log_entry.message[:40]} [...]'"

    if mssg_type in OPERATIONS:
        OPERATIONS.get(mssg_type)(log_entry)


def log_debug(message):
    logging.debug(message)


if __name__ == "__main__":
    configure_logging()
    logging.debug('debug')
    logging.info('info')
    logging.warning('warning')
    logging.error('error')
    logging.critical('critical')