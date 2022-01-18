import unittest.mock

import pytest

from attack_surface_pypy.core import container


@pytest.fixture
def repository_mock():
    repository_mock = unittest.mock.Mock(name='repository-mock')
    repository_mock.load_from = unittest.mock.AsyncMock(side_effect=repository_mock)
    yield repository_mock


@pytest.fixture
def data_loader_mock():
    yield unittest.mock.Mock(name='data-loader-mock')


@pytest.fixture
def domain_mock():
    yield unittest.mock.Mock(name='domain-mock')


@pytest.fixture
def state_mock():
    state_mock = unittest.mock.Mock(name='state-mock')
    state_mock.file_path = 'some/'
    yield state_mock


@pytest.fixture
def container_object(state_mock):
    yield container.CloudSurfaceContainer.configure(state_mock)


def test_configure_class_method_works_as_factory_initializing_class_with_a_state(container_object, state_mock):
    assert isinstance(container_object, container.CloudSurfaceContainer)
    # fine with protected attribute instead of dealing with the init mock
    assert container_object._domain_state == state_mock


async def test_get_data_loader_returns_data_loader_object(container_object, data_loader_mock):
    data_loader = await container_object.get_data_loader(data_loader_mock)

    data_loader_mock.assert_called_once_with('some/')
    assert data_loader is data_loader_mock()


async def test_get_data_repository_returns_data_repository_object(
        container_object, repository_mock, data_loader_mock
):
    data_repository = await container_object.get_data_repository(repository_mock, data_loader_mock)

    repository_mock.load_from.assert_called_once_with(data_loader_mock())
    assert data_repository is repository_mock()


async def test_get_data_domain_returns_data_domain_object(
        container_object, domain_mock, repository_mock, data_loader_mock
):
    data_domain = await container_object.get_data_domain(domain_mock, repository_mock, data_loader_mock)

    domain_mock.assert_called_once_with(repository_mock())
    assert data_domain is domain_mock()
