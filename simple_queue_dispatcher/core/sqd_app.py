import asyncio

import loguru
import mongoengine
from dotenv import load_dotenv

from simple_queue_dispatcher.core.app_config import AppConfig
from simple_queue_dispatcher.core.telegram_bot import TelegramBot
from simple_queue_dispatcher.data import mongo_utils
from simple_queue_dispatcher.data.data_model_mongo import SQDQueueItemMongo, \
    SQDQueueInfoMongo
from simple_queue_dispatcher.data.data_model_pydantic import \
    SQDQueueItemMessage, SQDQueueInfoMessage, QueueChatType


class SQDApp:
    logger = loguru.logger.bind(component="TelegramBot")

    def __init__(self, config: AppConfig = None):
        if config is None:
            config = self._load_config()
        self.config = config
        self.db = self._connect_db()
        self.bot = TelegramBot(config.telegram_bot, app=self)

    def _load_config(self):
        load_dotenv()
        return AppConfig()

    def _connect_db(self):
        db_config = self.config.database
        return mongoengine.connect(db=db_config.name,  # alias = db_config.name
                                   host=db_config.conn_str)

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
    def add_queue(self, queue_name: str):
        mongo_utils.add_item(SQDQueueInfoMongo, name=queue_name)

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

    # ------------------------------------------------------
    # RUN
    # ------------------------------------------------------

    def run(self):
        self.logger.info("Starting SQDApp")
        asyncio.run(self.bot.run())
