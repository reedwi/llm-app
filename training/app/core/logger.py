import logging
from logging.handlers import SysLogHandler
import sys

APP_LOGGER_NAME = 'chatbot_training'

def setup_applevel_logger(logger_name = APP_LOGGER_NAME, file_name=None):
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    syslog = SysLogHandler(address=('logs6.papertrailapp.com', 11789))
    format = '%(name)s - %(message)s'
    formatter = logging.Formatter(format, datefmt='%b %d %H:%M:%S')

    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(formatter)
    sh.setLevel(logging.INFO)
    syslog.setFormatter(formatter)
    syslog.setLevel(logging.INFO)

    logger.handlers.clear()
    logger.addHandler(syslog)
    logger.addHandler(sh)
    
    sys.excepthook = handle_exception
    
    if file_name:
        fh = logging.FileHandler(file_name)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger

def get_logger(module_name):    
   return logging.getLogger(APP_LOGGER_NAME).getChild(module_name)