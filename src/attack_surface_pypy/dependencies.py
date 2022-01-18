import fastapi
import starlette.requests
import starlette.datastructures

from attack_surface_pypy.core import container, probes, analytics


async def get_state(request: starlette.requests.Request) -> starlette.requests.State:
    return request.state


async def get_container(request: starlette.requests.Request) -> container.CloudSurfaceContainer:
    return request.app.state.container


async def get_probe(
        request: starlette.requests.Request,
        container_: container.CloudSurfaceContainer = fastapi.Depends(get_container)
):
    probe_instrumentality = await container_.get_probe_instrumentality()
    return probe_instrumentality.register_probe(
        request.scope['path'],
        probes.RouteProbe,
        analytics_factory=analytics.RouteAnalytics
    )
