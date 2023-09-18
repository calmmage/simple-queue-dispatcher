# run the app
from simple_queue_dispatcher.core.app import SQDApp
from bot_base.data_model.mongo_utils import connect_to_db
from bot_base.utils.logging_utils import setup_logger

if __name__ == '__main__':
    # connect to db
    connect_to_db()

    # setup logger
    setup_logger()

    app = SQDApp()
    app.run()
