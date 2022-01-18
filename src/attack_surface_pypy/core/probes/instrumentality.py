import types
import typing

import structlog

T = typing.TypeVar('T', bound="BaseProbe")


class ProbingInstrumentality:

    def __init__(self):
        self._registered_components = {}

    @classmethod
    def init(cls):
        return cls()

    def register_probe(
            self,
            name: str,
            probe_klass: typing.Type[T],
            logger_factory: typing.Callable[[], typing.Any] = structlog.get_logger,
            analytics_factory: typing.Callable[[], typing.Any] = types.SimpleNamespace,
    ) -> T:
        component = probe_klass(logger_factory, analytics_factory)
        if name not in self._registered_components:
            self._registered_components[name] = component
        return self._registered_components[name]