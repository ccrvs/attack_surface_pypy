from attack_surface_pypy.core.probes import base


class DomainProbe(base.BaseProbe):

    def inited(self, vms_count, fw_rules_count):
        self._analytics.vms_count = vms_count
        self._analytics.fw_rules_count = fw_rules_count
        self._logger.debug('domain.inited', vms_count=vms_count, fw_rules_count=fw_rules_count)

    def got_attacker_for(self, vm_id):
        self._logger.debug('domain.got_attacker_for', vm_id=vm_id)

    def got_attacker_to_victim_tags(self):
        self._logger.debug('domain.got_attacker_to_victim_tags')

    def got_attackers_for_victims_tags(self):
        self._logger.debug('domain.got_attackers_for_victims_tags')
