import logging
import logging.handlers

LOG_FILENAME = 'notebox/logs/notebox.log'

# Set up a specific logger with our desired output level
logger = logging.getLogger('notebox')
logger.setLevel(logging.DEBUG)

# Add the log message handler to the logger
file_handler = logging.handlers.RotatingFileHandler(
              LOG_FILENAME, maxBytes=1000000 * 24, backupCount=5)
file_handler.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(file_handler)