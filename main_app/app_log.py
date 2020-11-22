import logging
from shared import loggers


def get_logger(file_name, name='app'):
    log = loggers.get(name, None)
    if log is None:
        f_s = '%(asctime)s - %(name)s -  %(levelname)s - %(message)s'

        # logger
        log = logging.getLogger(name)

        # if not log.hasHandlers():
        log.setLevel(logging.DEBUG)

        # formatter
        f = logging.Formatter(f_s, datefmt='%d-%m-%Y %H:%M:%S')

        # handlers
        s_handler = logging.StreamHandler()
        f_handler = logging.FileHandler(file_name, encoding='utf-8')

        s_handler.setFormatter(f)
        f_handler.setFormatter(f)

        s_handler.setLevel(logging.DEBUG)
        f_handler.setLevel(logging.INFO)

        log.addHandler(s_handler)
        log.addHandler(f_handler)

        log.propagate = False

        loggers[name] = log

    return log
