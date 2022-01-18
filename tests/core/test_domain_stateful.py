import pytest
from hypothesis import strategies as st, assume, settings
import hypothesis.stateful

from attack_surface_pypy.core import domain, repository
from attack_surface_pypy.models.v1.models import firewall, vm, cloud, tag


TagsStrategy = st.lists(st.builds(tag.TagModel, name=st.text()), unique=True, min_size=2)
CloudStrategy = TagsStrategy.flatmap(
    lambda tags: st.tuples(
        st.lists(
            st.builds(
                vm.VMModel,
                vm_id=st.from_regex(r'^vm-\w{6,10}$'),
                tags=st.frozensets(st.sampled_from(tags)),
                name=st.text()
            ), unique_by=lambda vm_: vm_.vm_id, min_size=1
        ),
        st.lists(
            st.builds(
                firewall.FirewallRuleModel,
                fw_id=st.from_regex(r'^fw-\w{6,10}$'),
                source_tag=st.sampled_from(tags),
                dest_tag=st.sampled_from(tags),
            ).filter(lambda fw: fw.source_tag != fw.dest_tag), unique_by=lambda fw: fw.fw_id, min_size=1
        ),
    )
)


@pytest.mark.slow
@settings(max_examples=2000)
class DomainMachine(hypothesis.stateful.RuleBasedStateMachine):
    Repository = hypothesis.stateful.Bundle('Repository')
    VM = hypothesis.stateful.Bundle('VM', consume=True)
    Rule = hypothesis.stateful.Bundle('Rule')

    @hypothesis.stateful.initialize(target=Repository, data=CloudStrategy)
    def initialize(self, data):
        vms, fw_rules = data
        cloud_ = cloud.CloudEnvironmentModel(vms=vms, fw_rules=fw_rules)
        return repository.CloudDataRepository(cloud_)

    @hypothesis.stateful.rule(target=VM, repository_=Repository)
    def add_vms(self, repository_):
        return hypothesis.stateful.multiple(*repository_.get_vms())

    @hypothesis.stateful.rule(target=Rule, repository_=Repository)
    def add_rules(self, repository_):
        return hypothesis.stateful.multiple(*repository_.get_firewall_rules())

    @hypothesis.stateful.rule(
        repository_=Repository,
        victim_vm=VM,
        attackers_vms=st.sets(hypothesis.stateful.consumes(VM), min_size=1).filter(
            lambda vm_: st.deferred(lambda: rule.source_tag in vm_.tags)
        ),
        rule=Rule
    )
    def get_vm_attackers(self, repository_, victim_vm, attackers_vms, rule):
        assume(rule.dest_tag in victim_vm.tags)
        assume(all(rule.source_tag in attacker.tags for attacker in attackers_vms))

        assert domain.CloudSurfaceDomain(repository_).get_attackers_for_vm_id(victim_vm.vm_id).intersection({
            attacker.vm_id for attacker in attackers_vms
        })


DomainTest = DomainMachine.TestCase
