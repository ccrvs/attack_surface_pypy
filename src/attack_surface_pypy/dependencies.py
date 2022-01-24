import fastapi
import starlette.datastructures
import starlette.requests

from attack_surface_pypy.core import analytics, container, probes


def get_state(request: starlette.requests.Request) -> starlette.requests.State:
    return request.state


def get_container(request: starlette.requests.Request) -> container.CloudSurfaceContainer:
    return request.app.state.container


def get_probe_instrumentality(
        container_: container.CloudSurfaceContainer = fastapi.Depends(get_container)
) -> probes.ProbingInstrumentality:
    return container_.get_probe_instrumentality()


def get_probe(
        instrumentality: probes.ProbingInstrumentality = fastapi.Depends(get_probe_instrumentality)
) -> probes.RouteProbe:
    return instrumentality.register_probe(
        "Route",
        probes.RouteProbe,
        analytics_factory=analytics.RouteAnalytics
    )
