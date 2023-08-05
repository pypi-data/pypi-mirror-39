from ._abc import MessageABC


class ActorioException(Exception):
    pass


class NoLongerScheduled(ActorioException):
    pass


class EndMainLoop(ActorioException):
    pass


class UnhandledMessage(ActorioException, NotImplementedError):
    def __init__(self, message: MessageABC, *args: object) -> None:
        self.message = message
        super().__init__(*args)
