import structlog

from attack_surface_pypy.core.probes import base

logger = structlog.get_logger()


class RepositoryProbe(base.BaseProbe):

    def inited(self):
        logger.debug("repository.inited")

    def loaded(self, from_):
        logger.debug("repository.loaded", from_=from_)

    def vm_got(self, vm_id):
        logger.debug("repository.vm_got", vm_id=vm_id)

    def error(self, error):
        logger.error("repository.error", error=error)

    def rules_got(self):
        logger.debug("repository.rules_got")

    def vms_got(self):
        logger.debug("repository.vms_got")

    def accessed_vm_map(self):
        logger.debug("repository.accessed_vm_map")
