import asyncio
import typing

import fastapi
import starlette.datastructures

from attack_surface_pypy import protocols


class FastAPIApplication(fastapi.FastAPI, protocols.ASGIApplicationProto):
    ...


class Application(protocols.ApplicationProto):

    def __init__(
        self,
        app_factory: typing.Type[FastAPIApplication] = FastAPIApplication,
        **kwargs,
    ) -> None:
        self._app = app_factory(**kwargs)

        self._on_startup: typing.Set[typing.Callable[[], typing.Any]] = set()
        self._on_teardown: typing.Set[typing.Callable[[], typing.Any]] = set()

    async def __call__(self, *args, **kwargs) -> None:
        # self._register_components()
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

    def init_components(self, *components: protocols.InitializableProto) -> None:
        for component in components:
            self._on_startup.add(component.init)
            self._on_teardown.add(component.dispose)

    def register_exception_handler(
        self,
        exception_object: typing.Type[Exception],
        handler: typing.Callable[[typing.Any, typing.Type[Exception]], typing.Coroutine]
    ) -> None:
        self._register_exception_handler(exception_object, handler)

    async def _startup(self) -> None:
        return await self._gather(*self._on_startup)

    async def _teardown(self) -> None:
        return await self._gather(*self._on_teardown)

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

    def _register_components(self) -> None:
        self._app.on_event("startup")(self._startup)
        self._app.on_event("shutdown")(self._teardown)

    async def _gather(self, *tasks: typing.Callable) -> None:
        return await asyncio.gather(*(task() for task in tasks))
