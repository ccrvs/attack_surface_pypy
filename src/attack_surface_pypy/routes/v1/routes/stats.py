import uuid

import fastapi
import starlette.requests
import starlette.status

from attack_surface_pypy import dependencies
from attack_surface_pypy.core import probes
from attack_surface_pypy.models.v1.models import stats as stats_models

router = fastapi.APIRouter(prefix="/v1")


@router.get(
    "/stats/",
    tags=[
        "stats",
    ],
    name="Surface stats endpoint.",
    status_code=starlette.status.HTTP_200_OK,
    response_model=stats_models.StatsResponseModel,
)
async def stats(
    probe: probes.RouteProbe = fastapi.Depends(dependencies.get_probe),
    state: starlette.requests.State = fastapi.Depends(dependencies.get_state),
    domain_probe: probes.DomainProbe = fastapi.Depends(dependencies.get_domain_probe),
):
    state.id = request_id = uuid.uuid4().hex
    with probe.trace_request(request_id):
        routes_analytics = probe.analytics
        domain_analytics = domain_probe.analytics
        vms_count = domain_analytics.vms_count
        avg_response_time = routes_analytics.get_mean_response_time()
        requests_count = routes_analytics.get_requests_count()
        return stats_models.StatsResponseModel(
            request_count=requests_count,
            average_request_time=avg_response_time,
            vm_count=vms_count,
        )
