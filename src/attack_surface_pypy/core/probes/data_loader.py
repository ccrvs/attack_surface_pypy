from attack_surface_pypy.core.probes import base


class DataLoaderProbe(base.BaseProbe):

    def inited(self, timeout, path):
        self._logger.debug("data_loader.inited", path=str(path), timeout=timeout)

    def read(self, path):
        self._logger.debug("data_loader.read", path=str(path))

    def loaded(self, path):
        self._logger.info("data_loader.loaded", path=str(path))

    def error(self, error):
        self._logger.error("data_loader.error", error=str(error))

    def failed(self, error):
        self._logger.error("data_loader.failed", error=str(error))