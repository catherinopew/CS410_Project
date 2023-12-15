import logging
from flask import Flask
from logging.handlers import RotatingFileHandler


class AppLogger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppLogger, cls).__new__(cls)
        return cls._instance

    def __init__(self, logger_name, log_level=logging.DEBUG, log_file="app.log"):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(log_level)

        formatter = logging.Formatter('%(asctime)s - {app_name} - %(levelname)s - %(message)s')

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)
