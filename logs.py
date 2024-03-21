import logging
from logging.handlers import RotatingFileHandler
import os

current_path = os.path.abspath(os.path.curdir)
logs_folder = current_path + '/logs'

# create folder for logs
try:
    os.mkdir(logs_folder)
except FileExistsError: pass

formatter = logging.Formatter("[%(asctime)s] (%(levelname)s) %(message)s")

# console logger for all messages
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)

# file logger for all messages
file_handler = RotatingFileHandler(logs_folder + '/app_logs.log', 'a', maxBytes=10485760, backupCount=2)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

logger = logging.getLogger('default')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.addHandler(file_handler)


if __name__ == "__main__":
    logger.debug('Message!')
    logger.critical('Critical msg!')