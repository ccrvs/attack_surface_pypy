import fastapi
import starlette.requests
import starlette.status

from attack_surface_pypy import dependencies
from attack_surface_pypy.core import probes
from attack_surface_pypy.models.v1.models import stats as stats_models

router = fastapi.APIRouter(prefix="/v1")


@router.get(
    "/stats/",
    tags=["stats", ],
    name="Surface stats endpoint.",
    status_code=starlette.status.HTTP_200_OK,
    response_model=stats_models.StatsResponseModel,
)
async def stats(
        probe: probes.RouteProbe = fastapi.Depends(dependencies.get_probe),
        instrumentality: probes.ProbingInstrumentality = fastapi.Depends(dependencies.get_probe_instrumentality),
        state: starlette.requests.State = fastapi.Depends(dependencies.get_state),
):
    # probe.request('/stats/', state.id)
    domain_analytics = instrumentality.get_probe("CloudSurfaceDomain").analytics
    routes_analytics = probe.analytics
    vms_count = domain_analytics.vms_count
    avg_response_time = routes_analytics.get_mean_response_time()
    requests_count = routes_analytics.get_requests_count()
    # probe.response('/stats/', state.id, starlette.status.HTTP_200_OK)
    return stats_models.StatsResponseModel(
        request_count=requests_count,
        average_request_time=avg_response_time,
        vm_count=vms_count
    )
