from attack_surface_pypy import app as main_app
from attack_surface_pypy import app_factory
from attack_surface_pypy.core import container, probes


def create_app(path):
    return app_factory.init_app(
        path, main_app.Application, container.CloudSurfaceContainer, probes.ProbingInstrumentality
    )
