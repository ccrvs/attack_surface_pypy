import collections
import gc
import sys
import urllib.parse

import orjson
import uvicorn

from attack_surface_pypy import asgi, settings
from attack_surface_pypy.core import (
    container,
    data_loader,
    domain,
    probes,
    repository,
)
from attack_surface_pypy.logging import get_default_logging_config, structlog

gc.disable()

logger = structlog.get_logger()
cloud_container = container.CloudSurfaceContainer.configure(
    collections.namedtuple("State", "file_path")(".fixtures/input-3.json"),
    domain.CloudSurfaceDomain,
    repository.CloudDataRepository,
    data_loader.CloudDataJSONFileLoader,
    probes.ProbingInstrumentality,
)
cloud_container.init()
cloud_domain = cloud_container.get_data_domain()

start_404 = {"type": "http.response.start", "status": 404, "headers": [[b"content-type", b"application/json"], ]}
start_200 = {"type": "http.response.start", "status": 200, "headers": [[b"content-type", b"application/json"], ]}
body_404 = {
    "type": "http.response.body",
    "body": b"{}",
}


async def app(scope, receive, send):
    assert scope["type"] == "http"

    if scope["path"].startswith("/api/v1/attack"):
        query_params = urllib.parse.parse_qs(scope["query_string"])
        vm_ids = query_params.get(b"vm_id", None)
        if vm_ids is None:
            await _yield_404(send)
        vm_id, = vm_ids
        vm_id = vm_id.decode("utf-8")
        try:
            vms_ids = cloud_domain.get_attackers_for_vm_id(vm_id)
            await _yield_200(send, data=list(vms_ids))
            return
        except Exception:
            ...
    await _yield_404(send)


async def _yield_404(send):
    await send(start_404)
    await send(body_404)


async def _yield_200(send, data=None):
    data = data or {}
    await send(start_200)
    await send({
        "type": "http.response.body",
        "body": orjson.dumps(data),
    })


def run_uvicorn(file_path):
    uvicorn.run(
        lambda: asgi.create_app(path=file_path),
        # loop='uvloop',
        http="httptools",
        host=settings.service.host,
        port=settings.service.port,
        log_config=get_default_logging_config(settings.log_level),
        reload=settings.autoreload,
        debug=settings.debug,
        access_log=settings.debug,
        backlog=settings.backlog,
        factory=True,
    )


if __name__ == "__main__":
    _, path = sys.argv  # TODO: pass structure with initial values
    # sys.exit(run_uvicorn(file_path=path))  # TODO: hardcoded name, awry fabric
    uvicorn.run(app, access_log=False, debug=False, http="httptools", log_config=get_default_logging_config("ERROR"))
