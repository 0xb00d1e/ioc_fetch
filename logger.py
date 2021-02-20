import logging
import os
from logging.handlers import TimedRotatingFileHandler


def get_logger(name):
    logger = logging.getLogger(name)
    if not logger.handlers:
        this_dir = os.path.dirname(os.path.abspath(__file__))
        log_file = os.path.join(this_dir, 'logs', f'{name}.log')
        logger.setLevel(logging.DEBUG)
        file_handler = TimedRotatingFileHandler(
            log_file,
            when='d',
            interval=7,
            backupCount=52
        )
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    return logger
