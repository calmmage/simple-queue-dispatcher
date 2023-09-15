import mongomock
import pytest
from mongoengine import connect, disconnect

from simple_queue_dispatcher.data.data_model_mongo import SQDQueueItemMongo
from simple_queue_dispatcher.data.mongo_utils import (add_item, get_item,
                                                      update_item, delete_item)


@pytest.fixture(scope='function')
def mock_db():
    disconnect()
    connect(db='myTestDB',  # alias='test_db',
            mongo_client_class=mongomock.MongoClient)
    yield
    disconnect(  # alias='test_db'
    )


def test_add_item(mock_db):
    add_item(SQDQueueItemMongo, name='test_item', url='test_url')
    item = SQDQueueItemMongo.objects().last()
    assert item.name == 'test_item'
    assert item.url == 'test_url'


def test_get_item(mock_db):
    item = add_item(SQDQueueItemMongo, name='test_item')
    retrieved_item = get_item(SQDQueueItemMongo, 'test_item')
    assert item.id == retrieved_item.id


def test_update_item(mock_db):
    item = add_item(SQDQueueItemMongo, name='test_item', url='test_url')
    update_item(SQDQueueItemMongo, str(item.id), url='updated_url')
    updated_item = get_item(SQDQueueItemMongo, str(item.id))
    assert updated_item.url == 'updated_url'


def test_delete_item(mock_db):
    item = add_item(SQDQueueItemMongo, name='test_item')
    delete_item(SQDQueueItemMongo, str(item.id))
    deleted_item = get_item(SQDQueueItemMongo, str(item.id))
    assert deleted_item is None
