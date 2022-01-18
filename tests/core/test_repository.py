import unittest.mock

import pytest

from attack_surface_pypy import types
from attack_surface_pypy.models.v1.models import cloud, vm, firewall, tag

from attack_surface_pypy.core import repository, exceptions

_LOADER_SENTINEL = object()


@pytest.fixture
def vms_property_mock():
    yield unittest.mock.PropertyMock(return_value=[])


@pytest.fixture
def fws_property_mock():
    yield unittest.mock.PropertyMock(return_value=[])


@pytest.fixture
def cloud_data_mock(vms_property_mock, fws_property_mock):
    cloud_data_mock = unittest.mock.Mock(name='cloud-data-mock', spec=cloud.CloudEnvironmentModel)
    type(cloud_data_mock).vms = vms_property_mock
    type(cloud_data_mock).fw_rules = fws_property_mock
    yield cloud_data_mock


@pytest.fixture
def loader_mock(cloud_data_mock):
    loader_mock = unittest.mock.Mock(name='loader-mock')
    loader_mock.load = unittest.mock.AsyncMock(name='load-mock', return_value=cloud_data_mock)
    yield loader_mock


@pytest.fixture
async def repository_object(loader_mock):
    yield await repository.CloudDataRepository.load_from(loader_mock)


async def test_load_from_method_actually_calls_load_method_from_passed_loader_object(loader_mock, repository_object):
    assert loader_mock.load.called
    assert isinstance(repository_object, repository.CloudDataRepository)


async def test_load_from_method_instantiates_self_with_loaded_data(loader_mock, cloud_data_mock):
    with unittest.mock.patch.object(repository.CloudDataRepository, '__new__') as new_mock:
        await repository.CloudDataRepository.load_from(loader_mock)
    new_mock.assert_called_once_with(repository.CloudDataRepository, cloud_data_mock)


async def test_get_vm_by_id_method_return_required_vm_by_its_id_from_prepared_map(loader_mock):
    vm_stub = object()
    with unittest.mock.patch(  # because of __slots__ we can't mock a property of the already created object
            "attack_surface_pypy.core.repository.CloudDataRepository.vm_id_to_vm_map",
            new_callable=unittest.mock.PropertyMock
    ) as vm_id_map_mock:
        vm_id_map_mock.return_value = {'some_id': vm_stub}
        repository_object = await repository.CloudDataRepository.load_from(loader_mock)
        assert repository_object.get_vm_by_id(types.VM_ID('some_id')) == vm_stub
        vm_id_map_mock.assert_called_once()


async def test_get_vm_by_id_method_on_unknown_key_raises_vm_not_found_error(loader_mock):
    with unittest.mock.patch(  # because of __slots__ we can't mock a property of the already created object
            "attack_surface_pypy.core.repository.CloudDataRepository.vm_id_to_vm_map",
            new_callable=unittest.mock.PropertyMock
    ) as vm_id_map_mock:
        vm_id_map_mock.return_value = {}
        repository_object = await repository.CloudDataRepository.load_from(loader_mock)
        with pytest.raises(exceptions.VMNotFoundError) as exc_info:
            repository_object.get_vm_by_id(types.VM_ID('any_id'))
        assert exc_info.value.args[0] == f"VM with the given id `any_id` is not found."


async def test_get_vms_returns_all_the_vms_from_cloud_data_loaded(repository_object, cloud_data_mock):
    assert repository_object.get_vms() == cloud_data_mock.vms


async def test_get_firewall_rules_returns_all_the_fw_rules_from_cloud_data_loaded(repository_object, cloud_data_mock):
    assert repository_object.get_firewall_rules() == cloud_data_mock.fw_rules


async def test_vm_id_to_vm_map_gather_its_data_from_the_list_of_vms(repository_object, vms_property_mock):
    vm_mock = unittest.mock.Mock(name='vm-mock')
    vm_mock.vm_id = 'some_id'
    vms_property_mock.return_value = [vm_mock, ]
    assert repository_object.vm_id_to_vm_map == {'some_id': vm_mock}
