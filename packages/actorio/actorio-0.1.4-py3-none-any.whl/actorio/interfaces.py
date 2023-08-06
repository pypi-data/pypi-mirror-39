from typing import NewType

Name = NewType("Name", str)
Identifier = NewType("Identifier", str)


class Identified:
    def __init__(self, *args, identifier: Identifier, **kwargs):

        super().__init__(*args, **kwargs) # type: ignore
        self._identifier = identifier

    @property
    def identifier(self) -> Identifier:
        return self._identifier
