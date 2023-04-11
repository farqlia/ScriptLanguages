import logging
import sys
from labs.lab5.src.analyze_ssh_logs import MessageType

logging_level = {
    MessageType.BREAK_IN_ATTEMPT: logging.CRITICAL,
    MessageType.UNSUCCESSFUL_LOGIN: logging.WARNING,
    MessageType.INCORRECT_PASSWORD: logging.ERROR,
    MessageType.INCORRECT_USERNAME: logging.ERROR,
    MessageType.SUCCESSFUL_LOGIN: logging.INFO,
    MessageType.CLOSED_CONNECTION: logging.INFO
}

logging.basicConfig(level=logging.DEBUG)

logging_format = '%[(levelname)s]: %(asctime)s - %(message)s'
formatter = logging.Formatter(logging_format)
error_handler = logging.StreamHandler(sys.stderr)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)

console_handler = logging.StreamHandler(sys.stdin)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)


logger = logging.getLogger(__name__)
logger.addHandler(error_handler)
logger.addHandler(console_handler)
