from bot_base.core import App
from bot_base.data_model import mongo_utils

from simple_queue_dispatcher.core.app_config import SQDAppConfig
from simple_queue_dispatcher.core.telegram_bot import SQDTelegramBot
from simple_queue_dispatcher.data_model.dm_mongo import SQDQueueItemMongo, \
    SQDQueueInfoMongo
from simple_queue_dispatcher.data_model.dm_pydantic import \
    SQDQueueItemMessage, SQDQueueInfoMessage, QueueChatType, GetQueueResponse


class SQDApp(App):
    _app_config_class = SQDAppConfig
    _telegram_bot_class = SQDTelegramBot

    def __init__(self, config: _app_config_class = None):
        super().__init__(config)

    # ------------------------------------------------------
    # API
    # ------------------------------------------------------
    def add_item(self, item: SQDQueueItemMessage):
        mongo_item = SQDQueueItemMongo(
            name=item.name,
            description=item.description,
            url=item.url,
            queue_name=item.queue_name
        )
        mongo_item.save()

    def get_item(self, key: str) -> SQDQueueItemMessage:
        mongo_item = mongo_utils.get_item(key)
        return SQDQueueItemMessage(
            name=mongo_item.name,
            description=mongo_item.description,
            url=mongo_item.url,
            queue_name=mongo_item.queue_name
        )

    def update_item(self, key: str, update: SQDQueueItemMessage):
        mongo_utils.update_item(SQDQueueItemMongo, key, name=update.name,
                                description=update.description,
                                url=update.url,
                                queue_name=update.queue_name)

    def list_items(self, **filters):
        mongo_items = mongo_utils.list_items(SQDQueueItemMongo, **filters)
        return [SQDQueueItemMessage(
            name=mongo_item.name,
            description=mongo_item.description,
            url=mongo_item.url,
            queue_name=mongo_item.queue_name
        ) for mongo_item in mongo_items]

    # ------------------------------------------------------
    # API - queues
    # ------------------------------------------------------
    def add_queue(self, request: SQDQueueInfoMessage):
        mongo_utils.add_item(SQDQueueInfoMongo, name=request.name)
        self.update_queue(request)

    def update_queue(self, update: SQDQueueInfoMessage):
        if update.chat_type == QueueChatType.Input:
            mongo_utils.update_item(SQDQueueInfoMongo, update.name,
                                    input_chat_id=update.chat_id)
        elif update.chat_type == QueueChatType.Output:
            mongo_utils.update_item(SQDQueueInfoMongo, update.name,
                                    output_chat_id=update.chat_id)
        elif update.chat_type == QueueChatType.Archive:
            mongo_utils.update_item(SQDQueueInfoMongo, update.name,
                                    archive_chat_id=update.chat_id)

    def list_queues(self, **filters):
        return mongo_utils.list_items(SQDQueueInfoMongo, **filters)

    def has_queue(self, queue_name: str):
        item = mongo_utils.get_item(SQDQueueInfoMongo, queue_name)
        return item is not None

    def get_queue(self, queue_name: str):
        item = mongo_utils.get_item(SQDQueueInfoMongo, queue_name)
        return GetQueueResponse(
            name=item.name,
            input_chat_id=item.input_chat_id,
            output_chat_id=item.output_chat_id,
            archive_chat_id=item.archive_chat_id
        )
