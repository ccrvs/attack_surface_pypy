import unittest.mock

import pytest

from attack_surface_pypy.core import data_loader, exceptions


@pytest.fixture(autouse=True)
def timeout_mock():  # no need to spawn a thread on each `load` method call
    timeout_mock = unittest.mock.MagicMock()
    with unittest.mock.patch('attack_surface_pypy.core.data_loader.utils.timeout', timeout_mock):
        yield timeout_mock


@pytest.fixture
def io_mock():
    io_mock = unittest.mock.Mock(name='io-mock')
    io_mock.read.return_value = "{}"
    yield io_mock


@pytest.fixture
def context_manager_mock(io_mock):
    cm_mock = unittest.mock.MagicMock(name='cm-mock')
    cm_mock.__enter__.return_value = io_mock
    yield cm_mock


@pytest.fixture(autouse=True)
def open_mock(context_manager_mock):
    open_mock = unittest.mock.Mock(name='open-mock', return_value=context_manager_mock)
    with unittest.mock.patch('attack_surface_pypy.core.data_loader.trio.open_file', open_mock):
        yield open_mock


@pytest.fixture
def parser_mock():
    parser_mock = unittest.mock.Mock(name='parser-mock')
    with unittest.mock.patch('attack_surface_pypy.core.data_loader.cloud.CloudEnvironmentModel.parse_raw', parser_mock):
        yield parser_mock


@pytest.fixture
def cloud_loader(open_mock, parser_mock, timeout_mock):
    yield data_loader.CloudDataJSONFileLoader(path='some/', probe=unittest.mock.Mock())


def test_data_loader_opens_file_at_required_path_and_reads_data(cloud_loader, open_mock, io_mock):
    with unittest.mock.patch('attack_surface_pypy.core.data_loader.cloud.CloudEnvironmentModel.parse_raw'):
        cloud_loader.load()

    open_mock.assert_called_once_with('some/', 'r')
    io_mock.read.assert_called_once()


def test_data_loader_passes_read_data_to_model_parser(cloud_loader, parser_mock):
    cloud_loader.load()

    parser_mock.assert_called_with("{}")


def test_data_loader_returns_object_created_by_model_parser(cloud_loader, parser_mock):
    parser_mock.return_value = expected_result = {}
    actual_result = cloud_loader.load()
    assert actual_result == expected_result


def test_timeout_charges_with_the_argument_passed_to_initializer_or_default_value_otherwise(
        timeout_mock, parser_mock
):
    expected_timeout = -1
    cloud_loader = data_loader.CloudDataJSONFileLoader(
        path='some/', timeout=expected_timeout, probe=unittest.mock.Mock()
    )
    cloud_loader.load()

    timeout_mock.assert_called_once_with(expected_timeout)


def test_timeout_charges_with_default_constant_if_any_hasnt_been_provided(cloud_loader, timeout_mock):
    cloud_loader.load()

    timeout_mock.assert_called_once_with(30)  # free invariance coverage!


def test_timeout_error_will_cause_domain_timeout_exceeded_error_with_initialization_timeout(timeout_mock):
    expected_timeout = -1
    timeout_mock.side_effect = TimeoutError()
    with pytest.raises(exceptions.TimeoutExceededError) as exc_info:
        data_loader.CloudDataJSONFileLoader(
            path='some/',
            timeout=expected_timeout,
            probe=unittest.mock.Mock()
        ).load()
    assert str(exc_info.value) == f'The timeout has exceeded in {expected_timeout} seconds.'


def test_type_error_will_cause_domain_invalid_file_data_error(cloud_loader, parser_mock):
    parser_mock.side_effect = TypeError()

    with pytest.raises(exceptions.InvalidFileDataError) as exc_info:
        cloud_loader.load()

    assert str(exc_info.value) == 'Unable to parse data at some/'


def test_os_error_will_cause_domain_internal_error(cloud_loader, open_mock):
    open_mock.side_effect = OSError()

    with pytest.raises(exceptions.InternalError) as exc_info:
        cloud_loader.load()

    assert str(exc_info.value) == 'An internal error has occurred.'


@pytest.mark.parametrize('_, exc', [
    ('Some syntax error', SyntaxError),
    ('Some value error', ValueError),
    ('Some bare exception', Exception),
])
def test_all_other_exceptions_will_cause_domain_internal_error(_, exc, cloud_loader, parser_mock):
    parser_mock.side_effect = exc()

    with pytest.raises(exceptions.InternalError):
        cloud_loader.load()
