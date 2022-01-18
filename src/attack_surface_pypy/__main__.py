import sys

import hypercorn.config
import hypercorn.trio
import trio

from attack_surface_pypy import settings, asgi
from attack_surface_pypy.logging import structlog, get_default_logging_config

logger = structlog.get_logger()


def run_hypercorn():
    config = hypercorn.config.Config()
    config.bind = [f"{settings.service.host}:{settings.service.port}", ]
    config.debug = settings.debug  # no work since hypercorn can't use a debug with the serve
    config.loglevel = settings.log_level
    config.accesslog = settings.access_log
    config.errorlog = settings.error_log
    config.worker_class = 'trio'
    config.logconfig_dict = get_default_logging_config(settings.log_level)
    config.access_log_format = '%(h)s#%(D)s#%(H)s#%(m)s#%(Uq)s#%(s)s#%(b)s#%(f)s#%(a)s'
    trio.run(hypercorn.trio.serve, asgi.create_app(), config)


if __name__ == "__main__":
    sys.exit(run_hypercorn())  # TODO: hardcoded name, awry fabric
