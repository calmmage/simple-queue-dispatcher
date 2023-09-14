from dotenv import load_dotenv
from mongoengine import connect

from simple_queue_dispatcher.app_config import AppConfig
from simple_queue_dispatcher.data_model import SQDQueueItem
from simple_queue_dispatcher.mongo_utils import add_item, get_item, update_item, \
    delete_item

load_dotenv()


# step 0: test databasefrom pydantic import BaseSettings


# step 1 - try connecting to db with mongoengine
app_config = AppConfig()

db_config = app_config.database

conn = connect(db=db_config.name,  # alias = db_config.name
               host=db_config.conn_str)


# ----------------------------------------------------------
# 3: define Mongo item class, test add, get, update, delete
# ----------------------------------------------------------


def main():
    # Print values to verify
    print(f"Database Connection String: {app_config.database.conn_str}")
    print(f"Database Name: {app_config.database.name}")

    # Test operations
    add_item(SQDQueueItem, name='item1', url='url1')
    item = get_item(SQDQueueItem, 'item1')
    print(item.to_json())  # Should print the item

    # Assuming you know the '_id' of the item you just inserted
    known_id = str(item.id)
    update_item(SQDQueueItem, known_id, url='new_url1')
    print(get_item(SQDQueueItem,
                   known_id).to_json())  # Should print the updated item

    delete_item(SQDQueueItem, known_id)
    print(get_item(SQDQueueItem, known_id))  # Should print None


if __name__ == '__main__':
    main()
