import fastapi
import starlette.status
import starlette.requests

from attack_surface_pypy import types, dependencies
from attack_surface_pypy.core import container, domain, data_loader, repository, exceptions, probes

router = fastapi.APIRouter(prefix='/v1')


@router.get(
    '/attack/',
    tags=['attack', ],
    name='Attack VM endpoint.',
    status_code=starlette.status.HTTP_200_OK
)
async def attack(
        vm_id: types.VM_ID,
        response: fastapi.Response,
        cloud_container: container.CloudSurfaceContainer = fastapi.Depends(dependencies.get_container),
        state: starlette.requests.State = fastapi.Depends(dependencies.get_state),
        probe: probes.RouteProbe = fastapi.Depends(dependencies.get_probe),
):
    probe.request('/attack/', state.id)
    cloud_domain = await cloud_container.get_data_domain(
        domain_klass=domain.CloudSurfaceDomain,
        loader_klass=data_loader.CloudDataJSONFileLoader,
        repository_klass=repository.CloudDataRepository,
    )
    try:
        vms_ids = cloud_domain.get_attackers_for_vm_id(vm_id)
        probe.response('/attack/', state.id, starlette.status.HTTP_200_OK)
        return vms_ids
    except exceptions.VMNotFoundError as e:
        response.status_code = starlette.status.HTTP_404_NOT_FOUND
        probe.error('/attack/', e, response.status_code)
