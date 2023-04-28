import logging
import os


class Logger:
    def __init__(self, name, level=logging.INFO, filename="chatty.log"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # create file handler and set logging level
        file_handler = logging.FileHandler(os.path.join(log_dir, filename))
        file_handler.setLevel(level)

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %('
                                      'levelname)s - %(message)s')

        # add formatter to handlers
        file_handler.setFormatter(formatter)

        # add handlers to logger
        self.logger.addHandler(file_handler)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)
