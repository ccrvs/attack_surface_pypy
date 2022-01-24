import typing

from attack_surface_pypy.models.v1.models import base, firewall, vm


class CloudEnvironmentModel(base.BaseModel):
    vms: typing.List[vm.VMModel]
    fw_rules: typing.List[firewall.FirewallRuleModel]
