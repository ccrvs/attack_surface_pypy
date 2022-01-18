import unittest.mock

import pytest
import trio

from attack_surface_pypy.core import utils


@pytest.fixture
def fail_after_mock():
    fail_after_mock = unittest.mock.MagicMock(name='trio-mock')
    with unittest.mock.patch('attack_surface_pypy.core.utils.trio.fail_after', fail_after_mock):
        yield fail_after_mock


def test_timeout_context_manager_actually_calls_trio_method(fail_after_mock):
    timeout_sentinel = -1

    with utils.timeout(timeout_sentinel):
        ...
    fail_after_mock.assert_called_once_with(timeout_sentinel)


def test_timeout_context_manager_raises_timeout_error_if_too_slow_error_occurred(fail_after_mock):
    fail_after_mock().__enter__.side_effect = trio.TooSlowError()
    with pytest.raises(TimeoutError):
        with utils.timeout(-1):
            ...
