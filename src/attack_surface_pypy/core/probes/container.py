import structlog

from attack_surface_pypy.core.probes import base

logger = structlog.get_logger()


class ContainerProbe(base.BaseProbe):

    def inited(self):
        logger.debug("container.inited")

    def configured(self):
        logger.info("container.configured")

    def component_acquired(self, component):
        logger.debug("container.component_inited", component=component)
