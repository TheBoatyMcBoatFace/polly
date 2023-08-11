import os
import logging

logger_name = 'Civic🗽GPT'

logger = logging.getLogger(logger_name)

# Check if logger already has handlers
if not logger.hasHandlers():
    log_level = os.environ.get('LOG_LEVEL', 'DEBUG')
    logger.setLevel(logging.getLevelName(log_level))

    # Create console handler and set level to info
    ch = logging.StreamHandler()
    ch.setLevel(logging.getLevelName(log_level))

    # Create formatter and add it to the handler
    formatter = logging.Formatter('%(name)s [%(levelname)s] %(message)s')
    ch.setFormatter(formatter)

    # Add the console handler to the logger
    logger.addHandler(ch)
