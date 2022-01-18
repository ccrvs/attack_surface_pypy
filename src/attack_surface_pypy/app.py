import typing

import fastapi
import starlette.types
import starlette.datastructures


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


class FastAPIApplication(fastapi.FastAPI, ASGIApplicationProto):
    ...


class Application(ApplicationProto):

    def __init__(
            self,
            app_factory: typing.Type[FastAPIApplication] = FastAPIApplication,
            **kwargs,
    ) -> None:
        self._app = app_factory(**kwargs)

    async def __call__(self, *args, **kwargs) -> None:
        return await self._app(*args, **kwargs)

    @property
    def state(self) -> starlette.datastructures.State:
        return self._app.state

    @state.setter
    def state(self, value: starlette.datastructures.State) -> None:
        self._app.state = value

    def register_routes(self, *routes, **kwargs) -> None:
        for route in routes:
            self._register_route(route, **kwargs)

    def register_middlewares(self, *middlewares: typing.Union[typing.Callable, typing.Coroutine]) -> None:
        for middleware in middlewares:
            self._register_middleware(middleware)

    def register_exception_handler(
            self,
            exception_object: typing.Type[Exception],
            handler: typing.Callable[[typing.Any, typing.Type[Exception]], typing.Coroutine]
    ) -> None:
        self._register_exception_handler(exception_object, handler)

    def _register_route(self, module, **kwargs) -> None:
        self._app.include_router(module.router, prefix="/api", **kwargs)

    def _register_middleware(self, middleware: typing.Union[typing.Callable, typing.Awaitable]) -> None:
        self._app.middleware("http")(middleware)

    def _register_exception_handler(
            self,
            exception_object: typing.Type[Exception],
            exception_handler: typing.Callable[[typing.Any, typing.Type[Exception]], typing.Coroutine]
    ) -> None:
        self._app.add_exception_handler(exception_object, exception_handler)
