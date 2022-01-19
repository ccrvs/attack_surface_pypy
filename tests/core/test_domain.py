import collections
import unittest.mock

import pytest
from hypothesis import strategies as st, given, note

from attack_surface_pypy.core import repository, domain
from attack_surface_pypy.models.v1.models import tag, vm, firewall, cloud


@st.composite
def cloud_surface_strategy(draw, tags_strategy=st.builds(tag.TagModel, name=st.text())):
    tags = draw(st.lists(tags_strategy, min_size=1))
    vms_strategy = st.lists(st.builds(
        vm.VMModel,
        vm_id=st.from_regex(r'^vm-\w{6,10}$'),
        name=st.text(),
        tags=st.frozensets(st.sampled_from(tags)),
    ), unique_by=lambda vm_: vm_.vm_id)
    source_sample = st.sampled_from(tags)
    fws_strategy = st.lists(st.builds(
        firewall.FirewallRuleModel,
        fw_id=st.from_regex(r'^fw-\w{6,10}$'),
        source_tag=source_sample,
        dest_tag=st.sampled_from(tags).filter(lambda x: x != source_sample)
    ), unique_by=lambda fw: fw.fw_id)
    return draw(st.builds(cloud.CloudEnvironmentModel, vms=vms_strategy, fw_rules=fws_strategy))


@pytest.mark.slow
@given(cloud_surface_strategy())
def test_get_attackers_from_vm_id_returns_all_the_attackers_against_vm_with_requested_id(cloud_environment):
    data_repository = repository.CloudDataRepository(cloud_environment, unittest.mock.Mock())
    cloud_domain = domain.CloudSurfaceDomain(data_repository, unittest.mock.Mock())

    for virtual_machine in data_repository.get_vms():
        note("vm: %s" % virtual_machine)
        vm_tags = virtual_machine.tags
        attackers_tags = {rule.source_tag for rule in data_repository.get_firewall_rules() if rule.dest_tag in vm_tags}
        expected_result = {vm_.vm_id for vm_ in data_repository.get_vms() if vm_.tags & attackers_tags}
        actual_result = cloud_domain.get_attackers_for_vm_id(virtual_machine.vm_id)
        assert expected_result == actual_result


@pytest.mark.slow
@given(cloud_surface_strategy())
def test_victim_tag_to_attackers_vms_map_contains_proper_relations(cloud_environment):
    data_repository = repository.CloudDataRepository(cloud_environment, unittest.mock.Mock())
    cloud_domain = domain.CloudSurfaceDomain(data_repository, unittest.mock.Mock())

    expected_map = collections.defaultdict(set)
    for virtual_machine in data_repository.get_vms():
        for vm_tag in virtual_machine.tags:
            for rule in data_repository.get_firewall_rules():
                if vm_tag == rule.source_tag:
                    expected_map[rule.dest_tag].add(virtual_machine)
    assert cloud_domain.victim_tag_to_attackers_vms_map == expected_map


@pytest.mark.slow
@given(cloud_surface_strategy())
def test_attacker_to_victim_tags_map_contains_proper_relations(cloud_environment):
    data_repository = repository.CloudDataRepository(cloud_environment, unittest.mock.Mock())
    cloud_domain = domain.CloudSurfaceDomain(data_repository, unittest.mock.Mock())
    expected_map = collections.defaultdict(set)
    for rule in data_repository.get_firewall_rules():
        expected_map[rule.source_tag].add(rule.dest_tag)
    actual_map = cloud_domain.attacker_to_victim_tags_map
    assert actual_map == expected_map
