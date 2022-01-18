import typing

import pydantic

from attack_surface_pypy import app as main_app, middlewares, utils, settings
from attack_surface_pypy.core import container, probes
from attack_surface_pypy.routes.v1.routes import attack as attack_route, stats as stats_route


def init_app(
        application: typing.Type[main_app.Application],
        components_container: typing.Type[container.CloudSurfaceContainer],
        probe_instrumentality: typing.Type[probes.ProbingInstrumentality]
):
    app = application(main_app.FastAPIApplication, title="Attack surface app.")
    app.state.container = components_container.configure(settings.domain, probe_instrumentality.init())
    app.register_routes(
        attack_route,
        stats_route,
    )
    app.register_middlewares(
        middlewares.mark_request_session,
        middlewares.count_elapsed_time,
    )
    app.register_exception_handler(pydantic.ValidationError, utils.validation_error_handler)
    return app
