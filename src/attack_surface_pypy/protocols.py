import typing

import starlette.datastructures
import starlette.types


class ASGIApplicationProto(typing.Protocol):

    async def __call__(
        self,
        scope: starlette.types.Scope,
        receive: starlette.types.Receive,
        send: starlette.types.Send,
    ) -> None:
        ...


class ApplicationProto(typing.Protocol):

    @property
    def state(self) -> starlette.datastructures.State:
        ...

    def register_routes(self, *routes, **kwargs) -> None:
        ...

    def register_middlewares(self, *middlewares) -> None:
        ...


class InitializableProto(typing.Protocol):

    def init(self) -> typing.Any:
        ...

    def dispose(self) -> typing.Any:
        ...
