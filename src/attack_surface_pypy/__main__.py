import argparse
import gc
import pathlib
import sys
import typing

import uvicorn

from attack_surface_pypy import asgi, settings, __version__, __service_name__
from attack_surface_pypy import logging as app_logging

# logger = structlog.get_logger()
gc.disable()


parser = argparse.ArgumentParser(description='App initial arguments.', prog=__service_name__)
parser.add_argument(
    '-f', '--file-path',
    help='provide path to a file with initial data.',
    type=pathlib.Path,
    metavar='.fixtures/xxx.json',
    required=True,
    choices=[
        pathlib.Path('.fixtures/input-1.json'),
        pathlib.Path('.fixtures/input-2.json'),
        pathlib.Path('.fixtures/input-3.json'),
        pathlib.Path('.fixtures/input-4.json'),
        pathlib.Path('.fixtures/input-5.json'),
    ],
)
parser.add_argument(
    '-n', '--host',
    help='set host for the service.',
    type=str,
    metavar='localhost',
)
parser.add_argument(
    '-p', '--port',
    type=int,
    help='set port for the service.',
)
parser.add_argument(
    '-v', '--version',
    action='version',
    version=f'%(prog)s {__version__}',
)


def run_uvicorn(app_settings: settings.Settings, log_config: typing.Optional[dict] = None):
    uvicorn.run(
        asgi.create_app(app_settings),
        # loop='uvloop',
        http="httptools",
        host=app_settings.service.host,
        port=app_settings.service.port,
        log_config=log_config or {},
        reload=app_settings.autoreload,
        debug=app_settings.debug,
        access_log=app_settings.debug,
        backlog=app_settings.backlog,
        factory=True,
    )


if __name__ == "__main__":
    ns = parser.parse_args()
    domain_settings = settings.Domain(file_path=ns.file_path)
    service_settings = settings.Service()
    if ns.host or ns.port:
        service_settings = settings.Service(host=ns.host, port=ns.port)
    app_settings = settings.Settings(domain=domain_settings, service=service_settings)
    log_config = app_logging.LoggingConfig(
        log_level=app_settings.log_level,
        traceback_depth=app_settings.traceback_depth
    ).prepare_logger()
    # context = types.Context(file_path=ns.file_path, host=ns.host, port=ns.port)  # TODO: update settings from args?
    sys.exit(run_uvicorn(app_settings, log_config))  # TODO: hardcoded name, awry fabric
