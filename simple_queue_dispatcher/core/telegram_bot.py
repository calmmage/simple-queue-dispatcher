import re
from datetime import datetime
from typing import Dict
from typing import TYPE_CHECKING

# from aiogram.types import Message
# from aiogram.utils.markdown import hbold
from aiogram import types
# todo: use decorator to mark commands and parse automatically
from bot_base.core import TelegramBot, mark_command

from simple_queue_dispatcher.core.app_config import TelegramBotConfig
from simple_queue_dispatcher.data_model.dm_pydantic import \
    SQDQueueItemMessage, SQDQueueInfoMessage

if TYPE_CHECKING:
    from simple_queue_dispatcher.core import SQDApp


class SQDTelegramBot(TelegramBot):
    def __init__(self, config: TelegramBotConfig = None, app: 'SQDApp' = None):
        super().__init__(config)
        self.app = app

        self._multi_message_mode = False
        self.messages_stack = []

    # async def on_setup(self, message: types.Message):
    #     # todo: call App instead of executing logic here.
    #     args = message.get_args().split()
    #     if len(args) < 3:
    #         await message.reply(
    #             "Please provide all three arguments: queue_name, chat_id, type.")
    #         return
    #
    #     queue_name, chat_id, chat_type = args
    #     # Validation and saving logic here
    #     # Save these to a MongoDB collection for future use
    #     await message.reply(
    #         f"Queue {queue_name} set with chat_id {chat_id} for {chat_type}")

    @mark_command(commands=['add'], description="Add item to queue")
    async def add_item(self, message: types.Message):
        self.logger.info(f"Adding item from message \"{message.md_text}\"",
                         user=message.from_user.username)
        item = self.parse_message(message)
        self.app.add_item(item)

    def parse_message(self, message: types.Message) -> SQDQueueItemMessage:
        # todo: extract media - photos, videos - content as well and save to
        #  Notion
        data = self._process_message_text(message)

        return SQDQueueItemMessage(
            **data
        )

    def _process_message_text(self, message: types.Message, message_text: str
    = None) -> Dict[str, str]:
        if message_text is None:
            message_text = self._extract_message_text(message)
        data = self._parse_message_text(message_text)

        if 'description' not in data:
            data['description'] = message_text
        if 'name' not in data:
            data['name'] = self._generate_name(message_text)
        if 'queue' not in data:
            data['queue'] = self._determine_queue(message)
        if 'url' not in data:
            data['url'] = self._extract_url(message_text)
        return data

    recognized_hashtags = {  # todo: add tags or type to preserve info
        '#idea': {'queue': 'ideas'},
        '#task': {'queue': 'tasks'},
        '#shopping': {'queue': 'shopping'},
        '#recommendation': {'queue': 'recommendations'},
        '#feed': {'queue': 'feed'},
        '#content': {'queue': 'content'},
        '#feedback': {'queue': 'feedback'}
    }

    @staticmethod
    def _generate_name(message_text: str) -> str:
        # topic + date
        # todo: generate name with gpt (3?)
        topic = message_text.strip().split('\n')[0].replace(' ', '-').lower()

        date = datetime.now().strftime("%Y-%m-%d")
        return f"{topic}-{date}"

    @staticmethod
    def _determine_queue(message: types.Message) -> str:
        # for now - default
        # todo: use chat_id -> queue mapping
        return 'default'
        # todo: determine queue based on message content
        # option 1: use gpt (send message text and list of queues with
        # descriptions)
        # option 2: use gpt with function-calling (allow gpt to peek into ?

    url_re = re.compile(r'https?://(?:[-\w.]|%[\da-fA-F]{2})+')

    def _extract_url(self, message_text, message: types.Message = None):
        # option 1: if message contains url - extract it.
        # Support hidden links
        # message_text = message.md_text
        # todo: add support for multi-url case
        data = self.url_re.findall(message_text)
        if data:
            return data[0]

        # option 2: Save to Notion and then store Notion page url
        pass

        # option 3: If there's media content - save and add a link to it
        pass
        return None

    async def process_messages_stack(self):
        data = self._extract_stacked_messages_data()
        item = SQDQueueItemMessage(
            **data
        )
        self.app.add_item(item)

        self.logger.info(f"Messages processed, clearing stack")
        self.messages_stack = []

    async def process_message(self, message: types.Message):
        if self._multi_message_mode:
            self.messages_stack.append(message)
        else:
            # todo: make some smarter logic here. for example - pick between
            # add item and bulk add
            # automatically start multi-message mode
            await self.add_item(message)

    def bootstrap(self):
        super().bootstrap()
        # todo: simple message parsing
        # self.register_command(self.on_setup, commands=['setup'])
        self.register_command(self.add_item, commands=['add'])
        # todo: /setup command
        # todo: /bulkadd command

    # ------------------------------------------------------
    # New Commands
    # ------------------------------------------------------

    @mark_command(commands=['addqueue'], description="Add a new queue")
    def add_queue(self, message: types.Message):
        raise NotImplementedError

    @mark_command(commands=['register'], description="Setup a new queue")
    async def register_queue(self, message: types.Message):
        """
        # register a new chat config
        # components:
        #  1) queue = . default = defaut
        #  2) chat_id = defualt = this chat
        #  3) type = default = output
        # idea:
        #  possible chat connection type
        #  1) Input
        #  2) Output
        #  3) Archive
        """
        message_text = self._extract_message_text(message)
        data = self._parse_message_text(message_text)
        if 'queue' not in data:
            data['queue'] = 'default'
        if 'chat_id' not in data:
            data['chat_id'] = message.chat.id
        if 'type' not in data:
            data['type'] = 'output'

        item = SQDQueueInfoMessage(**data)
        if self.app.has_queue(item.name):
            self.app.update_queue(item)
        else:
            self.app.add_queue(item)

    @mark_command(commands=['bulkadd'],
                  description="Add multiple items to queue")
    async def bulk_add(self, message: types.Message):
        # Idea: split a single message into multiple items and process them
        #  one by one. Use gpt to split the message into multiple items?
        # Simple MVP: split by newlines, -
        # bonus: sub-items with indentationbul

        # todo: hard - support multi-message mode

        # todo: bonus - add an option to #guess automatically

        # todo: request missing data one by one
        raise NotImplementedError

    @mark_command()
    async def get(self, message: types.Message):
        """
        Get item using provided info appropriately
        - If there's key - get by key
        - if #random - get random item
        - if nothing - get latest
        """
        pass

    @mark_command()
    async def get_item(self, message: types.Message):
        """
        # get item by id / key
        """
        pass
