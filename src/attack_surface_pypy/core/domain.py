import collections
import functools
import typing

import structlog

from attack_surface_pypy import types
from attack_surface_pypy.core import graph, repository, probes
from attack_surface_pypy.models.v1.models import vm, tag

AttackerToVictimTagsMapType = typing.DefaultDict[
    tag.TagModel, typing.Set[tag.TagModel]
]
VictimTagToAttackersVMsMapType = typing.DefaultDict[
    tag.TagModel, typing.Set[vm.VMModel]
]
logger = structlog.get_logger()


class CloudSurfaceDomain:
    __slots__ = '_repository', '_graph', '_probe'

    def __init__(self, data_provider: repository.CloudDataRepository, probe: probes.DomainProbe):
        self._repository = data_provider
        self._probe = probe

        vms = data_provider.get_vms()
        fw_rules = data_provider.get_firewall_rules()
        self._graph = graph.CloudGraph(vms=vms, firewall_rules=fw_rules)

        self._probe.inited(vms_count=len(vms), fw_rules_count=len(fw_rules))

    @functools.lru_cache()  # TODO: remove, just for test
    def get_attackers_for_vm_id(
            self,
            vm_id: types.VM_ID,
    ) -> typing.Set[vm.VMModel]:
        self._probe.got_attacker_for(vm_id=vm_id)
        target_vm = self._repository.get_vm_by_id(vm_id=vm_id)

        return {
            attacker_vm.vm_id
            for vm_tag in target_vm.tags
            for attacker_vm in self.victim_tag_to_attackers_vms_map[vm_tag]
        }

    @property  # type: ignore  # https://github.com/python/mypy/issues/1362
    @functools.lru_cache()
    def attacker_to_victim_tags_map(self) -> AttackerToVictimTagsMapType:
        self._probe.got_attacker_to_victim_tags()
        return self._get_attacker_to_victim_tags_map()

    @property  # type: ignore
    @functools.lru_cache()
    def victim_tag_to_attackers_vms_map(
            self
    ) -> VictimTagToAttackersVMsMapType:
        self._probe.got_attackers_for_victims_tags()
        return self._get_victim_tag_to_attackers_vms_map()

    def _get_victim_tag_to_attackers_vms_map(
            self,
    ) -> VictimTagToAttackersVMsMapType:
        tags_edges_iter = self._graph.traverse_tags_edges()

        victim_tag_to_attacker_vms_map: VictimTagToAttackersVMsMapType = collections.defaultdict(set)
        for attacker_tag, virtual_machine in tags_edges_iter:
            for victim_tag in self.attacker_to_victim_tags_map[attacker_tag]:  # type: ignore  # sigh, lru_cache again
                victim_tag_to_attacker_vms_map[victim_tag].add(virtual_machine)
        return victim_tag_to_attacker_vms_map

    def _get_attacker_to_victim_tags_map(self) -> AttackerToVictimTagsMapType:
        firewall_rules_iter = self._graph.traverse_firewall_rules_edges()

        attacker_to_victim_tags_map = collections.defaultdict(set)
        for attacker_tag, victim_tag in firewall_rules_iter:
            attacker_to_victim_tags_map[attacker_tag].add(victim_tag)
        return attacker_to_victim_tags_map
