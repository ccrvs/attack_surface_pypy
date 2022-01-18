from hypothesis import strategies as st, given, note

from attack_surface_pypy.core import graph
from attack_surface_pypy.models.v1.models import vm, tag, firewall


@st.composite
def fws_strategy(draw, tags_strategy=st.builds(tag.TagModel, name=st.text())):
    tags = draw(st.lists(tags_strategy, min_size=1))
    source_sample = st.sampled_from(tags)
    return draw(st.lists(st.builds(
        firewall.FirewallRuleModel,
        fw_id=st.from_regex(r'^fw-\w{6,10}$'),
        source_tag=source_sample,
        dest_tag=st.sampled_from(tags).filter(lambda x: x != source_sample)
    )))


@st.composite
def vms_strategy(draw, tags_strategy=st.builds(tag.TagModel, name=st.text())):
    tags = draw(st.lists(tags_strategy, min_size=1))
    return draw(st.lists(st.builds(
        vm.VMModel,
        vm_id=st.from_regex(r'^vm-\w{6,10}$'),
        name=st.text(),
        tags=st.frozensets(st.sampled_from(tags)),
    )))


@given(vms_strategy())
def test_traverse_tags_edges_returns_all_the_tags_edges_within_graph(vms):
    note(f"Test VMs: {vms!s}")
    test_graph = graph.CloudGraph(vms, [])
    assert list(test_graph.traverse_tags_edges()) == [(tag_, vm_) for vm_ in vms for tag_ in vm_.tags]


@given(fws_strategy())
def test_traverse_firewall_rules_edges_returns_all_the_rules_edges_within_graph(fws):
    note(f"Test FWs: {fws!s}")
    test_graph = graph.CloudGraph([], fws)
    assert list(test_graph.traverse_firewall_rules_edges()) == [(rule.source_tag, rule.dest_tag) for rule in fws]
