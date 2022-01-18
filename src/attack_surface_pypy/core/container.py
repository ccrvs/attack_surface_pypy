from __future__ import annotations

import asyncstdlib.functools as functools
import typing

from attack_surface_pypy.logging import structlog
from attack_surface_pypy.core import repository, domain, data_loader, probes
from attack_surface_pypy.settings import Domain

logger = structlog.get_logger()


class CloudSurfaceContainer:

    def __init__(self, domain_state: Domain, probe_instrumentality: probes.ProbingInstrumentality) -> None:
        self._domain_state = domain_state
        self._probe_instrumentality = probe_instrumentality
        self._probe = self._probe_instrumentality.register_probe('ContainerProbe', probes.ContainerProbe)

    @classmethod
    def configure(
            cls,
            domain_state: Domain,
            probe_instrumentality: probes.ProbingInstrumentality,
    ) -> CloudSurfaceContainer:
        instance = cls(domain_state, probe_instrumentality)
        instance._probe.inited()
        return instance

    @functools.lru_cache
    async def get_data_loader(
            self,
            loader_klass: typing.Type[data_loader.CloudDataJSONFileLoader]
    ) -> data_loader.CloudDataJSONFileLoader:
        probe = self._probe_instrumentality.register_probe('CloudDataJSONFileLoader', probes.DataLoaderProbe)
        data_loader_object = loader_klass(self._domain_state.file_path, probe)
        self._probe.component_inited(component=loader_klass.__name__)  # TODO: suppress loudmouther for tests
        return data_loader_object

    @functools.lru_cache
    async def get_data_repository(
            self,
            repository_klass: typing.Type[repository.CloudDataRepository],
            loader_klass: typing.Type[data_loader.CloudDataJSONFileLoader],
    ) -> repository.CloudDataRepository:
        loader = await self.get_data_loader(loader_klass)
        probe = self._probe_instrumentality.register_probe('CloudDataRepository', probes.RepositoryProbe)
        data_repository_object = await repository_klass.load_from(loader, probe)
        self._probe.component_inited(component=repository_klass.__name__)
        return data_repository_object

    @functools.lru_cache
    async def get_data_domain(
            self,
            domain_klass: typing.Type[domain.CloudSurfaceDomain],
            repository_klass: typing.Type[repository.CloudDataRepository],
            loader_klass: typing.Type[data_loader.CloudDataJSONFileLoader],
    ) -> domain.CloudSurfaceDomain:
        probe = self._probe_instrumentality.register_probe('CloudSurfaceDomain', probes.DomainProbe)
        data_repository = await self.get_data_repository(repository_klass, loader_klass)  # type: ignore
        domain_object = domain_klass(data_repository, probe)
        self._probe.component_inited(component=domain_klass.__name__)
        return domain_object

    async def get_probe_instrumentality(self) -> probes.ProbingInstrumentality:
        return self._probe_instrumentality
