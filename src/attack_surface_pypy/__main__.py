import sys

import uvicorn

from attack_surface_pypy import settings, asgi
from attack_surface_pypy.logging import structlog, get_default_logging_config

logger = structlog.get_logger()


def run_uvicorn(file_path):
    uvicorn.run(
        lambda: asgi.create_app(path=file_path),
        loop='uvloop',
        http='httptools',
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
    sys.exit(run_uvicorn(file_path=path))  # TODO: hardcoded name, awry fabric
