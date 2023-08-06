import uuid

from actorio._abc import IdentifiedABC, IdentifierABC


class Identifier(str, IdentifierABC):
    def __repr__(self):
        return "{class_name}({value})".format(class_name=self.__class__.__name__, value=str(self))


class Identified(IdentifiedABC):
    """
    Base implementation of :class: `IdentifiedABC`, constructor will automatically create a :class: `Identifier` from a uuid4 if none is provided.
    """

    def __init__(self, *args, identifier: IdentifierABC = None, **kwargs) -> None:
        super().__init__()
        self.identifier = identifier or Identifier(uuid.uuid4())
