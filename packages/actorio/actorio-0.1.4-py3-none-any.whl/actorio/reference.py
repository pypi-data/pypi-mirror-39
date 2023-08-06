import asyncio
from typing import Union

from actorio._abc import ReferenceABC, IdentifierABC, ActorReferenceABC, MessageABC, MessageQueueABC
from actorio.interfaces import Identified, Identifier
from actorio.messaging import MessageQueue


class ActorReference(ActorReferenceABC):

    def __init__(self, *args, actor_id: IdentifierABC, actor_inbox: MessageQueueABC, **kwargs) -> None:
        super().__init__(*args, **kwargs)  # type: ignore
        self.actor_inbox = actor_inbox
        self.actor_id = actor_id

    @property
    def identifier(self) -> IdentifierABC:
        return self.actor_id

    async def tell(self, message: MessageABC) -> None:
        await self.actor_inbox.put(message)

    async def ask(self, message: MessageABC, *, timeout: float = None) -> MessageABC:
        # FIXME: it works for now, but it will probably break application-logic code if mixed with `tell`.

        # this method only wait for the first response message, it should be used carefully if referenced actor wants to send multiple answers
        # it might be better to keep the sender id and just set a `reply_to` field for this request only

        if message.sender:
            identifier = message.sender.identifier
        else:
            identifier = Identifier()

        temporary_reference = Reference(identifier=identifier)
        message.sender = temporary_reference
        await self.tell(message)
        return await asyncio.wait_for(temporary_reference.inbox.get(), timeout=timeout)


async def ask(actor_ref: ActorReferenceABC, message: MessageABC, timeout: Union[float, int] = None) -> MessageABC:
    return await actor_ref.ask(message, timeout=timeout)


class Reference(ReferenceABC, Identified):

    def __init__(self, *args, identifier: IdentifierABC = None, **kwargs) -> None:
        super().__init__(*args, identifier=identifier, **kwargs)
        self.inbox = MessageQueue()

    async def tell(self, message: MessageABC) -> None:
        await self.inbox.put(message)
