from .pool import DBHandler
from .rmq import RMQHandler
from .utils import *


def create_pool():
    db_handler = DBHandler()
    db_handler.get_connection()

    return db_handler

def create_rmq():
    rmq_handler = RMQHandler()
    rmq_handler.connect()

    rmq_handler.channel.queue_declare(queue="ws_messages")
    rmq_handler.channel.queue_declare(queue="scraper_messages")

    return rmq_handler

db_handler = create_pool()
rmq_handler = create_rmq()

# @app.teardown_appcontext
# def teardown_appcontext(exception=None):
#     db_handler.db_pool.closeall()
#     rmq_handler.close_connection()