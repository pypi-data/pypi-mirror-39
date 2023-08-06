import datetime
from abc import ABC, abstractmethod
from typing import Optional


class IdentifierABC(ABC):
    @abstractmethod
    def __hash__(self): pass

    @abstractmethod
    def __eq__(self, other): pass

    @abstractmethod
    def __str__(self): pass

    def as_string(self) -> str:
        return str(self)


class IdentifiedABC(ABC):
    """Identified objects"""

    identifier: IdentifierABC

    def has_same_identifier(self, other: "IdentifiedABC") -> bool:
        return other.identifier == self.identifier

    def __hash__(self):
        return hash(self.identifier)

    def __eq__(self, other):
        if isinstance(other, IdentifiedABC):
            return self.has_same_identifier(other)
        return NotImplemented


class ActorABC(IdentifiedABC):
    inbox: "MessageQueueABC"
    reference: "ActorReferenceABC"

    @abstractmethod
    async def stop(self) -> None:
        """Tell the :class: `Actor` to stop handling events,
        it will finish processing its current event before
        calling its `mainloop_teardown` async method
        
        This method is called outside of the actor context."""

    @abstractmethod
    async def start(self) -> None:
        """Tell the :class: `Actor` to start handling events.

        This method is called outside of the actor context."""

    @abstractmethod
    async def wait(self) -> None:
        """Wait until the :class: `Actor` object stops."""

    async def run_until_stopped(self) -> None:
        """Start the :class: `Actor` object and wait until it's stopped."""
        async with self:
            await self

    def __await__(self):
        return self.wait().__await__()

    async def __aenter__(self) -> "ActorReferenceABC":
        await self.start()
        return self.reference

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stop()


class ReferenceABC(IdentifiedABC):
    @abstractmethod
    async def tell(self, message: "MessageABC") -> None: pass


class ActorReferenceABC(ReferenceABC):
    @abstractmethod
    async def tell(self, message: "MessageABC") -> None: pass

    @abstractmethod
    async def ask(self, message: "MessageABC", *, timeout: float = None) -> "MessageABC": pass


class MessageABC(ABC):
    sender: Optional[ReferenceABC]
    creation_date: datetime.datetime

    async def reply(self, message: "MessageABC"):
        await self.sender.tell(message)


class MessageQueueABC(ABC):
    async def put(self, item: MessageABC) -> None: pass

    def put_nowait(self, item: MessageABC) -> None: pass

    async def get(self) -> MessageABC: pass

    def get_nowait(self) -> MessageABC: pass
