import logging
from flask import Flask
from logging.handlers import RotatingFileHandler

# Singleton class for managing the application logger
class AppLogger:
    _instance = None

    def __new__(cls):
        # Singleton pattern: Ensure only one instance of AppLogger is created
        if cls._instance is None:
            cls._instance = super(AppLogger, cls).__new__(cls)
        return cls._instance

    def __init__(self, logger_name, log_level=logging.DEBUG, log_file="app.log"):
        # Initialize the logger with specified name, log level, and log file
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(log_level)

        formatter = logging.Formatter('%(asctime)s - {app_name} - %(levelname)s - %(message)s')

        # Add a console handler with the specified log format
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # Add a rotating file handler with maxBytes and backupCount settings
        file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def debug(self, message):
        # Log a message with the DEBUG level
        self.logger.debug(message)

    def info(self, message):
        # Log a message with the INFO level
        self.logger.info(message)

    def warning(self, message):
        # Log a message with the WARNING level
        self.logger.warning(message)

    def error(self, message):
        # Log a message with the ERROR level
        self.logger.error(message)

    def critical(self, message):
        # Log a message with the CRITICAL level
        self.logger.critical(message)
