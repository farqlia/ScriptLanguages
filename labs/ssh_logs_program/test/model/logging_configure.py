import sys

import labs.ssh_logs_program.src.model.logging_configure as logging_configure
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging_configure.error_handler)
logger.addHandler(logging_configure.console_handler)

logging.debug('debug')
logging.info('info')
logging.warning('warning')
logging.error('error')
logging.critical('critical')