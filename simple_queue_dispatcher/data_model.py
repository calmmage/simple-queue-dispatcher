from mongoengine import Document, StringField


class SQDQueueItem(Document):
    name = StringField(required=True)
    url = StringField(required=False)

    meta = {'collection': 'sqd_queue_items'}  # Explicitly set collection name
