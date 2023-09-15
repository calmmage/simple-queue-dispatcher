from enum import Enum
from typing import Optional

from pydantic import BaseModel


class SQDQueueItemMessage(BaseModel):
    name: str  # = Field(..., description='Name of the queue item')
    description: Optional[str] = None  # = Field(..., description='Description
    # of the queue item')
    queue_name: Optional[str] = None  # = Field(..., description='Name of the
    # queue',
    url: Optional[
        str] = None  # = Field(..., description='URL of the queue item')

    # required=False)

    class Config:
        json_schema_extra = {
            'example': {
                'name': 'item1',
                'url': 'url1',
                'description': 'description1',
                'queue_name': 'queue1'
            }
        }


class QueueChatType(Enum):
    Input = 'input'
    Output = 'output'
    Archive = 'archive'


class SQDQueueInfoMessage(BaseModel):
    # queue_name, chat_id, chat_type
    name: str
    chat_id: str
    chat_type: QueueChatType
