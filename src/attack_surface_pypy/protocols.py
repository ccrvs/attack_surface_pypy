import typing


class InitializableProto(typing.Protocol):

    async def init(self) -> typing.Any:
        ...

    async def dispose(self) -> typing.Any:
        ...
