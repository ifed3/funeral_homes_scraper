"""Logger definition"""

import logging
import datetime

def create_logger(name):
    """Customizes the logger for use in all modules"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    curr_time = datetime.datetime.today().strftime("%m%d%Y %H-%M-%S")
    file_handler = logging.FileHandler('./logs/scraper ' + curr_time + '.log')
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s: %(name)-4s: %(levelname)-4s: %(message)s')
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    return logger

logger = create_logger(__name__)