import typing

import pydantic

from attack_surface_pypy import app as main_app, middlewares, utils, settings
from attack_surface_pypy.core import container, probes, data_loader, repository, domain
from attack_surface_pypy.routes.v1.routes import attack as attack_route, stats as stats_route


import guppy
heap = guppy.hpy()

def init_app(
        file_path: str,
        application: typing.Type[main_app.Application],
        components_container: typing.Type[container.CloudSurfaceContainer],
        probe_instrumentality_factory: typing.Type[probes.ProbingInstrumentality]
):
    from collections import namedtuple
    app = application(main_app.FastAPIApplication, title="Attack surface app.")
    cloud_container = components_container.configure(
        namedtuple('State', 'file_path')(file_path),
        domain.CloudSurfaceDomain,
        repository.CloudDataRepository,
        data_loader.CloudDataJSONFileLoader,
        probe_instrumentality_factory,
    )
    cloud_container.init()
    app.state.container = cloud_container
    # app.init_components(cloud_container)
    app.register_routes(
        attack_route,
        stats_route,
    )
    # app.register_middlewares(
        # middlewares.mark_request_session,
        # middlewares.count_elapsed_time,
        # middlewares.mark_request_session_and_elapsed_time_sec
    # )
    app.register_exception_handler(pydantic.ValidationError, utils.validation_error_handler)
    return app
