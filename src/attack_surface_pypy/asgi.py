from attack_surface_pypy import app as main_app, app_factory
from attack_surface_pypy.core import container, probes


def create_app():
    return app_factory.init_app(main_app.Application, container.CloudSurfaceContainer, probes.ProbingInstrumentality)
