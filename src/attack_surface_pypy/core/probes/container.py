from attack_surface_pypy.core.probes import base


class ContainerProbe(base.BaseProbe):

    def inited(self):
        self._logger.debug("container.inited")

    def configured(self):
        self._logger.info("container.configured")

    def component_inited(self, component):
        self._logger.debug("container.component_inited", component=component)
