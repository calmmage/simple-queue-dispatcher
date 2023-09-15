from mongoengine import Document, StringField



class SQDQueueItemMongo(Document):
    name = StringField(required=True)
    url = StringField(required=False)
    description = StringField(required=False)
    queue_name = StringField(required=False)

    meta = {'collection': 'sqd_queue_items'}  # Explicitly set collection name


class SQDQueueInfoMongo(Document):
    name = StringField(required=True)
    input_chat_id = StringField(required=False)
    output_chat_id = StringField(required=True)
    archive_chat_id = StringField(required=False)

    meta = {'collection': 'sqd_queue_infos'}  # Explicitly set collection name


if __name__ == '__main__':
    # test mongo connection
    from simple_queue_dispatcher.data.mongo_utils import connect_to_db

    connect_to_db()
