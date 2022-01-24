"""
This module contains a single probes' instrumentality class.

ProbingInstrumentality -- a simple probes repository-like object.
"""

__all__ = ("ProbingInstrumentality", )

import types
import typing

import structlog

T = typing.TypeVar("T", bound="BaseProbe")


class ProbingInstrumentality:
    """ A class responsible for registration and acquiring already registered probes.

    Might be treated as the single point of registration or dispensing of any probes within the service. Initializes
    via the IoC container at the application startup stage and lives inside him.

    Example:
         >>> from attack_surface_pypy.core.probes import RepositoryProbe
         >>> instrumentality = ProbingInstrumentality()
         >>> repository_probe = instrumentality.register_probe('SomeComponent', RepositoryProbe)
         >>> assert repository_probe is instrumentality.get_probe('SomeComponent')
         True
    """

    def __init__(self) -> None:
        self._registered_components: dict[str, T] = {}

    def register_probe(
        self,
        name: str,
        probe_klass: typing.Type[T],
        analytics_factory: typing.Callable[[], typing.Any] = types.SimpleNamespace,
    ) -> T:
        """
        Instantiates a probe via the passed probe class either with the passed logger and analytics factories or
        with default otherwise. Saves the new probe inside a map.
        :param name: any key related to a probe to get this probe afterwards.
        :param probe_klass: a probe class.
        :param logger_factory: callable object returns a logger instance.
        :param analytics_factory: callable object returns an analytics instance.
        :return: a registered probe.
        """
        if name not in self._registered_components:
            component = probe_klass(analytics_factory)
            self._registered_components[name] = component
        return self._registered_components[name]

    def get_probe(self, name: str) -> T:
        """
        Acquire an already registered probe by the key.
        :param name: the name a probe were registered with.
        :return: a probe object.
        """
        return self._registered_components[name]  # TODO: ProbeNotFoundError
