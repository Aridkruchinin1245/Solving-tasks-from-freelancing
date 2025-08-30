import logging

logger = logging.getLogger()
file_handler = logging.FileHandler('logs/logs.log')
formatter = logging.Formatter(fmt='%(asctime)s %(levelname)s %(message)s')

logger.setLevel('DEBUG')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
