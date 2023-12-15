from logger import AppLogger

def create_logger():
    app_logger = AppLogger()

    return app_logger

app_logger = create_logger()