""" A module containing core containers objects.

CloudSurfaceContainer -- a simple implementation of the IoC container for the application components.
"""

from __future__ import annotations

__all__ = (
    'CloudSurfaceContainer',
)

import typing

import asyncstdlib.functools as functools

from attack_surface_pypy import protocols
from attack_surface_pypy.logging import structlog
from attack_surface_pypy.core import repository, domain, data_loader, probes
from attack_surface_pypy.settings import Domain

logger = structlog.get_logger()


class CloudSurfaceContainer(protocols.InitializableProto):

    def __init__(
            self,
            domain_state: Domain,
            domain_klass: typing.Type[domain.CloudSurfaceDomain],
            repository_klass: typing.Type[repository.CloudDataRepository],
            loader_klass: typing.Type[data_loader.CloudDataJSONFileLoader],
            probe_instrumentality: typing.Type[probes.ProbingInstrumentality],
    ) -> None:
        self._domain_state = domain_state
        self._domain_klass = domain_klass
        self._repository_klass = repository_klass
        self._loader_klass = loader_klass
        self._probe_instrumentality = probe_instrumentality()
        self._probe = self._probe_instrumentality.register_probe('ContainerProbe', probes.ContainerProbe)

    @classmethod
    def configure(
            cls,
            domain_state: Domain,
            domain_klass: typing.Type[domain.CloudSurfaceDomain],
            repository_klass: typing.Type[repository.CloudDataRepository],
            loader_klass: typing.Type[data_loader.CloudDataJSONFileLoader],
            probe_instrumentality: typing.Type[probes.ProbingInstrumentality],
    ) -> CloudSurfaceContainer:
        instance = cls(domain_state, domain_klass, repository_klass, loader_klass, probe_instrumentality)
        instance._probe.inited()
        return instance

    async def init(self,) -> None:
        await self.get_data_loader()
        await self.get_data_repository()
        await self.get_data_domain()

    async def dispose(self) -> None:
        ...

    @functools.lru_cache
    async def get_data_loader(self) -> data_loader.CloudDataJSONFileLoader:
        probe = self._probe_instrumentality.register_probe('CloudDataJSONFileLoader', probes.DataLoaderProbe)
        data_loader_object = self._loader_klass(self._domain_state.file_path, probe)
        self._probe.component_inited(component=self._loader_klass.__name__)  # TODO: suppress loudmouther for tests
        return data_loader_object

    @functools.lru_cache
    async def get_data_repository(self) -> repository.CloudDataRepository:
        loader = await self.get_data_loader()
        probe = self._probe_instrumentality.register_probe('CloudDataRepository', probes.RepositoryProbe)
        data_repository_object = await self._repository_klass.load_from(loader, probe)
        self._probe.component_inited(component=self._repository_klass.__name__)
        return data_repository_object

    @functools.lru_cache
    async def get_data_domain(self) -> domain.CloudSurfaceDomain:
        probe = self._probe_instrumentality.register_probe('CloudSurfaceDomain', probes.DomainProbe)
        data_repository = await self.get_data_repository()
        domain_object = self._domain_klass(data_repository, probe)
        self._probe.component_inited(component=self._domain_klass.__name__)
        return domain_object

    async def get_probe_instrumentality(self) -> probes.ProbingInstrumentality:
        return self._probe_instrumentality
