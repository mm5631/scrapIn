import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(level)% - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

def get_logger(name):
    return logging.getLogger(name)
