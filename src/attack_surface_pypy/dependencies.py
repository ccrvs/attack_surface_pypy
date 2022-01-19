import fastapi
import starlette.requests
import starlette.datastructures

from attack_surface_pypy.core import container, probes, analytics


async def get_state(request: starlette.requests.Request) -> starlette.requests.State:
    return request.state


async def get_container(request: starlette.requests.Request) -> container.CloudSurfaceContainer:
    return request.app.state.container


async def get_probe_instrumentality(
        container_: container.CloudSurfaceContainer = fastapi.Depends(get_container)
) -> probes.ProbingInstrumentality:
    return await container_.get_probe_instrumentality()


async def get_probe(
        instrumentality: probes.ProbingInstrumentality = fastapi.Depends(get_probe_instrumentality)
) -> probes.RouteProbe:
    return instrumentality.register_probe(
        'Route',
        probes.RouteProbe,
        analytics_factory=analytics.RouteAnalytics
    )
