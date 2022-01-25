import typing

from attack_surface_pypy import app as main_app
from attack_surface_pypy import app_factory, settings
from attack_surface_pypy.core import container


def create_app(app_settings: settings.Settings) -> typing.Callable[[], main_app.Application]:
    return lambda: app_factory.init_app(app_settings, main_app.Application, container.CloudSurfaceContainer)
