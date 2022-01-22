import typing


class InitializableProto(typing.Protocol):

    def init(self) -> typing.Any:
        ...

    def dispose(self) -> typing.Any:
        ...
