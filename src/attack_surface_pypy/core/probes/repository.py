from attack_surface_pypy.core.probes import base


class RepositoryProbe(base.BaseProbe):

    def inited(self):
        self._logger.debug('repository.inited')

    def loaded(self, from_):
        self._logger.debug('repository.loaded', from_=from_)

    def vm_got(self, vm_id):
        self._logger.debug('repository.vm_got', vm_id=vm_id)

    def error(self, error):
        self._logger.error('repository.error', error=error)

    def rules_got(self):
        self._logger.debug('repository.rules_got')

    def vms_got(self):
        self._logger.debug('repository.vms_got')

    def accessed_vm_map(self):
        self._logger.debug('repository.accessed_vm_map')
