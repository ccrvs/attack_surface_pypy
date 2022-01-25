""" A module containing core containers objects.

CloudSurfaceContainer -- a simple implementation of the IoC container for the application components.
"""

from __future__ import annotations

__all__ = ("CloudSurfaceContainer", )

import typing

from attack_surface_pypy import settings
from attack_surface_pypy.core import data_loader, domain, probes, repository
from attack_surface_pypy.logging import structlog

logger = structlog.get_logger()


class CloudSurfaceContainer:
    __slots__ = ('_data_loader', '_data_repository', '_data_domain', '_probe_instrumentality', '_configured', '_probe', )

    def __init__(self, probe: probes.ContainerProbe) -> None:
        self._probe = probe
        self._configured = False

        self._data_loader: typing.Optional[data_loader.CloudDataJSONFileLoader] = None
        self._data_repository: typing.Optional[repository.CloudDataRepository] = None
        self._data_domain: typing.Optional[domain.CloudSurfaceDomain] = None
        self._probe_instrumentality: typing.Optional[probes.ProbingInstrumentality] = None

        self._probe.inited()

    @classmethod
    def configure(
        cls,
        context: settings.Domain,
        loader_klass: typing.Type[data_loader.CloudDataJSONFileLoader],
        repository_klass: typing.Type[repository.CloudDataRepository],
        domain_klass: typing.Type[domain.CloudSurfaceDomain],
        probe_instrumentality_klass: typing.Type[probes.ProbingInstrumentality],
    ) -> CloudSurfaceContainer:
        probe_instrumentality = probe_instrumentality_klass()
        probe = probe_instrumentality.register_probe(cls.__name__, probes.ContainerProbe)
        loader_probe = probe_instrumentality.register_probe(loader_klass.__name__, probes.DataLoaderProbe)
        repository_probe = probe_instrumentality.register_probe(repository_klass.__name__, probes.RepositoryProbe)
        domain_probe = probe_instrumentality.register_probe(domain_klass.__name__, probes.DomainProbe)

        self = cls(probe)
        self._configured = True
        self._data_loader = data_loader = loader_klass(context.file_path, probe=loader_probe)
        self._data_repository = data_repository = repository_klass.load_from(data_loader, probe=repository_probe)
        self._data_domain = domain_klass(data_repository, probe=domain_probe)
        self._probe_instrumentality = probe_instrumentality

        probe.configured()
        return self

    def get_data_loader(self) -> typing.Optional[data_loader.CloudDataJSONFileLoader]:
        assert self._configured, "The class must be configured first."
        self._probe.component_acquired(component='data_loader')
        return self._data_loader

    def get_data_repository(self) -> typing.Optional[repository.CloudDataRepository]:
        assert self._configured, "The class must be configured first."
        self._probe.component_acquired(component='data_repository')
        return self._data_repository

    def get_data_domain(self) -> typing.Optional[domain.CloudSurfaceDomain]:
        assert self._configured, "The class must be configured first."
        self._probe.component_acquired(component='data_domain')
        return self._data_domain

    def get_probe_instrumentality(self) -> typing.Optional[probes.ProbingInstrumentality]:
        assert self._configured, "The class must be configured first."
        self._probe.component_acquired(component='probe_instrumentality')
        return self._probe_instrumentality
