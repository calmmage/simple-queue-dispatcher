"""
# Queue Operations with MongoDB and MongoEngine

This project demonstrates basic CRUD operations with MongoDB and MongoEngine.

## Use Cases

### Abstract Add
The `add_item` function allows for abstract addition of any class that inherits from MongoEngine's `Document`.

add_item(SQDQueueItem, name='item1', url='url1')

# Find an Item
Items can be fetched by either their _id or a name field.

get_item(SQDQueueItem, 'item1')  # By name
get_item(SQDQueueItem, '5ff751482749093351c3e90f')  # By _id

# Update an Item
Items can be updated by providing their _id or name and the fields to update.

update_item(SQDQueueItem, 'item1', url='new_url1')
update_item(SQDQueueItem, '5ff751482749093351c3e90f', url='new_url1')

# Delete an Item
Items can be deleted by providing their _id or name.
delete_item(SQDQueueItem, '5ff751482749093351c3e90f')
delete_item(SQDQueueItem, 'item1')

"""
from bson import ObjectId


def add_item(cls, **kwargs):
    item = cls(**kwargs)
    item.save()
    return item


def get_item(cls, key):
    try:
        # Try finding by ObjectId first
        return cls.objects(id=ObjectId(key)).first()
    except:
        # Fallback to find by name
        return cls.objects(name=key).first()


def update_item(cls, key, **kwargs):
    item = get_item(cls, key)
    if item:
        item.update(**kwargs)


def delete_item(cls, key):
    item = get_item(cls, key)
    if item:
        item.delete()
