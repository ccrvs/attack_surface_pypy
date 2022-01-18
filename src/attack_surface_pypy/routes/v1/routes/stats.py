import fastapi
import starlette.status
import starlette.requests

from attack_surface_pypy import types, dependencies
from attack_surface_pypy.core import container, domain, data_loader, repository, exceptions, probes

router = fastapi.APIRouter(prefix='/v1')


@router.get(
    '/stats/',
    tags=['stats', ],
    name='Surface stats endpoint.',
    status_code=starlette.status.HTTP_200_OK
)
async def attack(
        probe: probes.RouteProbe = fastapi.Depends(dependencies.get_probe),
):
    return probe._analytics.get_median_response_time()
