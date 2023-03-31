import logging
import os
from pathlib import Path

'''
DEBUG
INFO
WARNING
ERROR
CRITICAL
'''
if __name__ == '__main__':

    info_logfile = Path(os.getcwd()) / 'mylog.txt'
    logging.basicConfig(filename=info_logfile, encoding='utf-8',
                        level=logging.INFO)

    logging.info("INFO LOG")
    assert info_logfile.exists()
    with open(info_logfile) as f:
        print(f.readline())

    logging.debug("DEBUG LOG")