import datetime
from abc import ABC, abstractmethod
from typing import Union, Optional


class IdentifierABC(ABC):
    @abstractmethod
    def __hash__(self): pass

    @abstractmethod
    def __str__(self): pass

    def as_string(self) -> str:
        return str(self)


class IdentifiedABC(ABC):
    """
    Identified objects
    """

    identifier: IdentifierABC

    def has_same_identifier(self, other: "IdentifiedABC") -> bool:
        return other.identifier == self.identifier

    def __hash__(self):
        return hash(self.identifier)


class ActorABC(IdentifiedABC):
    inbox: "MessageQueueABC"
    reference: "ActorReferenceABC"

    @abstractmethod
    async def stop(self) -> None: pass

    @abstractmethod
    async def start(self) -> None: pass

    @abstractmethod
    async def wait(self) -> None: pass

    def __await__(self):
        return self.wait().__await__()

    async def __aenter__(self) -> "ActorReferenceABC":
        await self.start()
        return self.reference

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stop()


class ReferenceABC(IdentifiedABC):
    @abstractmethod
    async def tell(self, message: "MessageABC") -> None:
        pass


class ActorReferenceABC(ReferenceABC):
    @abstractmethod
    async def tell(self, message: "MessageABC") -> None:
        pass

    @abstractmethod
    async def ask(self, message: "MessageABC", *, timeout:Union[float, int]  = None) -> "MessageABC":
        pass


class MessageABC(ABC):
    sender: Optional[ReferenceABC]
    creation_date: datetime.datetime

class MessageABC(ABC):
    sender: Optional[ReferenceABC]
    creation_date: datetime.datetime

    async def reply(self, message: "MessageABC"):
        await self.sender.tell(message)


class MessageQueueABC(ABC):
    async def put(self, item: MessageABC) -> None:
        pass

    def put_nowait(self, item: MessageABC) -> None:
        pass

    async def get(self) -> MessageABC:
        pass

    def get_nowait(self) -> MessageABC:
        pass
