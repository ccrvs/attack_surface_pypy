import structlog

from attack_surface_pypy.core.probes import base

logger = structlog.get_logger()


class DataLoaderProbe(base.BaseProbe):

    def inited(self, timeout, path):
        logger.debug("data_loader.inited", path=str(path), timeout=timeout)

    def read(self, path):
        logger.debug("data_loader.read", path=str(path))

    def loaded(self, path):
        logger.info("data_loader.loaded", path=str(path))

    def error(self, error):
        logger.error("data_loader.error", error=str(error))

    def failed(self, error):
        logger.error("data_loader.failed", error=str(error))
