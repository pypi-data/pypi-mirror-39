import asyncio
import datetime
from typing import Union

from pytz import UTC

from ._abc import MessageABC, MessageQueueABC, ReferenceABC, ActorABC
from .errors import ActorioException


class Message(MessageABC):
    def __init__(self, *args, creation_date: datetime.datetime = None, sender: Union[ReferenceABC, ActorABC] = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)  # type: ignore
        self.creation_date = creation_date or datetime.datetime.utcnow().replace(tzinfo=UTC)
        if sender:
            self.sender = sender if isinstance(sender, ReferenceABC) else sender.reference
        else:
            self.sender = None


class MessageQueue(MessageQueueABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._queue = asyncio.Queue()

    async def put(self, message: MessageABC):
        if not message.sender:
            raise ActorioException("Message should have a sender")
        return await self._queue.put(message)

    def put_nowait(self, message: MessageABC):
        if not message.sender:
            raise ActorioException("Message should have a sender")
        return self._queue.put_nowait(message)

    async def get(self) -> MessageABC:
        return await self._queue.get()

    def get_nowait(self) -> MessageABC:
        return self._queue.get_nowait()


class DataMessage(Message):
    def __init__(self, *args, data, creation_date: datetime.datetime = None, sender: Union[ReferenceABC, ActorABC] = None, **kwargs) -> None:
        super().__init__(*args, creation_date=creation_date, sender=sender, **kwargs)
        self.data = data
