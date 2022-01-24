import typing

from attack_surface_pypy.models.v1.models import firewall, tag, vm


class CloudGraph:
    __slots__ = '_vms_nodes', '_firewall_rules_nodes',

    def __init__(
            self,
            vms: typing.Iterable[vm.VMModel],
            firewall_rules: typing.Iterable[firewall.FirewallRuleModel],
    ):
        self._vms_nodes = vms
        self._firewall_rules_nodes = firewall_rules

    def traverse_tags_edges(
            self,
    ) -> typing.Iterator[typing.Tuple[tag.TagModel, vm.VMModel]]:
        for vm_ in self._vms_nodes:
            for tag_ in vm_.tags:
                yield tag_, vm_

    def traverse_firewall_rules_edges(
            self,
    ) -> typing.Iterator[typing.Tuple[tag.TagModel, tag.TagModel]]:
        for rule in self._firewall_rules_nodes:
            yield rule.source_tag, rule.dest_tag
