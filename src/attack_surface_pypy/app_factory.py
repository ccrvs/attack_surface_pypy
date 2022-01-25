import typing

import pydantic

from attack_surface_pypy import app as main_app
from attack_surface_pypy import settings, utils
from attack_surface_pypy.core import (
    container,
    data_loader,
    domain,
    probes,
    repository,
)
from attack_surface_pypy.routes.v1.routes import attack as attack_route
from attack_surface_pypy.routes.v1.routes import stats as stats_route


def init_app(
    app_settings: settings.Settings,
    Application: typing.Type[main_app.Application],
    Container: typing.Type[container.CloudSurfaceContainer],
):
    app = Application(main_app.FastAPIApplication, title="Attack Surface App.")
    app.state.container = Container.configure(
        context=app_settings.domain,
        loader_klass=data_loader.CloudDataJSONFileLoader,
        domain_klass=domain.CloudSurfaceDomain,
        repository_klass=repository.CloudDataRepository,
        probe_instrumentality_klass=probes.ProbingInstrumentality,
    )
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
