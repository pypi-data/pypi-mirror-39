__version__ = '0.1.0'

LOGGER_ROOT = 'dophon_logger.'

COMMAND = {
    'name': 'command'
}

DOPHON = {
    'name': 'dophon',
}


def get_logger(logger_type: dict):
    logger = __import__(LOGGER_ROOT + logger_type['name'], fromlist=True)
    return logger
