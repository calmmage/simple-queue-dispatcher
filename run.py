# run the app
from simple_queue_dispatcher.core.sqd_app import SQDApp
from simple_queue_dispatcher.data.mongo_utils import connect_to_db
from simple_queue_dispatcher.utils.logging_utils import setup_logger

if __name__ == '__main__':
    # connect to db
    connect_to_db()

    # setup logger
    setup_logger()

    app = SQDApp()
    app.run()
