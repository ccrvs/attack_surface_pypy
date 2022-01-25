import uuid

import fastapi
import starlette.requests
import starlette.status

from attack_surface_pypy import dependencies, types
from attack_surface_pypy.core import (
    domain,
    exceptions,
    probes,
)

router = fastapi.APIRouter(prefix="/v1")


@router.get(
    "/attack/", tags=[
        "attack",
    ], name="Attack VM endpoint.", status_code=starlette.status.HTTP_200_OK
)
async def attack(
    vm_id: types.VM_ID,
    response: fastapi.Response,
    cloud_domain: domain.CloudSurfaceDomain = fastapi.Depends(dependencies.get_data_domain),
    state: starlette.requests.State = fastapi.Depends(dependencies.get_state),
    probe: probes.RouteProbe = fastapi.Depends(dependencies.get_probe),
):
    state.id = request_id = uuid.uuid4().hex
    with probe.trace_request(request_id):
        try:
            vms_ids = cloud_domain.get_attackers_for_vm_id(vm_id)
        except exceptions.VMNotFoundError:
            response.status_code = starlette.status.HTTP_404_NOT_FOUND
            return
        return vms_ids
