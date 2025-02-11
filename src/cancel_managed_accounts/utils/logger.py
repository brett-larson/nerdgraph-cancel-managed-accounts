import logging
import os
from datetime import datetime

def setup_logger(name: str) -> logging.Logger:
    """
    Setup a logger with a file handler.
    :param name: Name of the logger
    :return: Logger object
    """

    # Create logs directory if it doesn't exist
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    os.makedirs(log_dir, exist_ok=True)

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Prevent adding handlers multiple times
    if logger.handlers:
        return logger

    # Create formatter
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # File handler - using date in filename
    log_file = os.path.join(
        log_dir,
        f'app_{datetime.now().strftime("%Y%m%d")}.log'
    )

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(file_formatter)

    # Add file handler to logger
    logger.addHandler(file_handler)

    return logger
