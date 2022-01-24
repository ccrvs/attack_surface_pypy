from __future__ import annotations

import pathlib
import typing
import warnings

import structlog

from attack_surface_pypy import types
from attack_surface_pypy.core import data_loader, exceptions, probes
from attack_surface_pypy.models.v1.models import cloud, firewall, vm

logger = structlog.get_logger()


class CloudDataRepository:
    __slots__ = "_cloud_data", "_vm_id_to_vm_map", "_probe"

    def __init__(self, cloud_data: cloud.CloudEnvironmentModel, probe: probes.RepositoryProbe) -> None:
        self._cloud_data = cloud_data
        self._probe = probe

        self._vm_id_to_vm_map: typing.Optional[typing.MutableMapping[types.VM_ID, vm.VMModel]] = None

        self._probe.inited()

    @classmethod
    def load_from(cls, loader: data_loader.DataLoaderProto, probe) -> CloudDataRepository:
        cloud_data = loader.load()
        repository = cls(cloud_data, probe)
        repository._probe.loaded(from_=loader.__class__.__name__)
        return repository

    @classmethod
    def from_json(
        cls,
        path: typing.Union[str, pathlib.Path],
        probe,
    ) -> CloudDataRepository:
        warnings.warn(
            "Stale method, use `load_from` instead.", DeprecationWarning, stacklevel=2
        )  # FIXME: where s my warning?

        cloud_data = cloud.CloudEnvironmentModel.parse_file(path)
        return cls(cloud_data, probe)

    def get_vm_by_id(self, vm_id: types.VM_ID) -> vm.VMModel:
        self._probe.vm_got(vm_id=vm_id)
        try:
            return self.vm_id_to_vm_map[vm_id]
        except KeyError as e:
            self._probe.error(error=e)
            raise exceptions.VMNotFoundError(vm_id) from e

    def get_firewall_rules(self) -> typing.List[firewall.FirewallRuleModel]:
        self._probe.rules_got()
        return self._cloud_data.fw_rules

    def get_vms(self) -> typing.List[vm.VMModel]:
        self._probe.vms_got()
        return self._cloud_data.vms

    @property
    def vm_id_to_vm_map(self) -> typing.MutableMapping[types.VM_ID, vm.VMModel]:
        if self._vm_id_to_vm_map is None:
            self._vm_id_to_vm_map = {virtual_machine.vm_id: virtual_machine for virtual_machine in self.get_vms()}
        self._probe.accessed_vm_map()
        return self._vm_id_to_vm_map
