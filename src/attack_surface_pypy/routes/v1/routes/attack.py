import uuid

import fastapi
import starlette.requests
import starlette.status

from attack_surface_pypy import dependencies, types
from attack_surface_pypy.core import (
    container,
    data_loader,
    domain,
    exceptions,
    probes,
    repository,
)

router = fastapi.APIRouter(prefix="/v1")
import structlog

logger = structlog.get_logger()

@router.get(
    "/attack/",
    tags=["attack", ],
    name="Attack VM endpoint.",
    status_code=starlette.status.HTTP_200_OK
)
async def attack(
        vm_id: types.VM_ID,
        response: fastapi.Response,
        cloud_container: container.CloudSurfaceContainer = fastapi.Depends(dependencies.get_container),
        state: starlette.requests.State = fastapi.Depends(dependencies.get_state),
        # probe: probes.RouteProbe = fastapi.Depends(dependencies.get_probe),
):
    state.id = uuid.uuid4().hex
    # probe.request('/attack/', state.id)
    logger.info("/attack/", id_=state.id)
    cloud_domain = cloud_container.get_data_domain()
    try:
        vms_ids = cloud_domain.get_attackers_for_vm_id(vm_id)
        logger.info("/attack/", id_=state.id, status=starlette.status.HTTP_200_OK)
        # probe.response('/attack/', state.id, starlette.status.HTTP_200_OK)
        return vms_ids
    except exceptions.VMNotFoundError as e:
        response.status_code = starlette.status.HTTP_404_NOT_FOUND
        logger.info("/attack/", error=e, status=response.status_code)
        # probe.error('/attack/', e, response.status_code)
