import typing

from attack_surface_pypy.models.v1.models import base, vm, firewall


class CloudEnvironmentModel(base.BaseModel):
    vms: typing.List[vm.VMModel]
    fw_rules: typing.List[firewall.FirewallRuleModel]
