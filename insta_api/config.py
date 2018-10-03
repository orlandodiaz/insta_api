import logging
log = logging.getLogger(__name__)
root_logger = logging.getLogger('urllib3')


def configure_logger():
    print(log.handlers)
    if not log.handlers:
        print(logging.getLogger('__name__').handlers)

        # LOGGING FORMAT
        fmt = '[%(asctime)s %(filename)18s] %(levelname)-7s - %(message)7s'
        date_fmt = '%Y-%m-%d %H:%M:%S'
        formatter = logging.Formatter(fmt, datefmt=date_fmt)

        # STDOUT LOGGING
        stdout = logging.StreamHandler()
        stdout.setFormatter(formatter)

        log.addHandler(stdout)
        log.setLevel(logging.DEBUG)

        root_logger.addHandler(stdout)
        root_logger.setLevel(logging.DEBUG)

def log_to_file(log_path, logroot=True):
    """Redirect logging to a log file"""

    # LOGGING FORMAT
    fmt = '[%(asctime)s %(filename)18s] %(levelname)-7s - %(message)7s'
    date_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(fmt, datefmt=date_fmt)

    file_handler = logging.FileHandler(log_path)
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)

    if logroot:
        root_logger.addHandler(file_handler)
        root_logger.setLevel(logging.DEBUG)

def enable_logging():
    log.setLevel(logging.DEBUG)

def disable_logging():
    log.setLevel(logging.WARNING)
    root_logger.setLevel(logging.WARNING)

configure_logger()
# log_to_file("../logs/insta_api_new_log")