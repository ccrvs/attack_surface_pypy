import fastapi
import starlette.datastructures
import starlette.requests

from attack_surface_pypy.core import analytics, container, domain, probes


async def get_state(request: starlette.requests.Request) -> starlette.requests.State:
    return request.state


async def get_container(request: starlette.requests.Request) -> container.CloudSurfaceContainer:
    return request.app.state.container


async def get_data_domain(
    container_: container.CloudSurfaceContainer = fastapi.Depends(get_container)
) -> domain.CloudSurfaceDomain:
    return container_.get_data_domain()


async def get_probe_instrumentality(
    container_: container.CloudSurfaceContainer = fastapi.Depends(get_container)
) -> probes.ProbingInstrumentality:
    return container_.get_probe_instrumentality()


async def get_probe(
    instrumentality: probes.ProbingInstrumentality = fastapi.Depends(get_probe_instrumentality)
) -> probes.RouteProbe:
    return instrumentality.register_probe("Route", probes.RouteProbe, analytics_factory=analytics.RouteAnalytics)


async def get_domain_probe(
    instrumentality: probes.ProbingInstrumentality = fastapi.Depends(get_probe_instrumentality)
) -> probes.DomainProbe:
    return instrumentality.get_probe("CloudSurfaceDomain")
