import unittest.mock

import pytest
from hypothesis import strategies as st, settings, given, HealthCheck, note

from attack_surface_pypy import constants
from attack_surface_pypy.middlewares import request


@pytest.fixture
def uuid_mock():
    with unittest.mock.patch('attack_surface_pypy.middlewares.request.uuid') as uuid_mock:
        yield uuid_mock


@pytest.fixture
def request_mock():
    request_mock = unittest.mock.Mock(name='request-mock')
    request_mock.state = unittest.mock.Mock(name='state-mock')
    yield request_mock


@pytest.fixture
def response_mock():
    response_mock = unittest.mock.Mock(name='response-mock')
    response_mock.headers = {}
    yield response_mock


@pytest.fixture
def call_next(response_mock):
    async def _call_next_stub(_):
        return response_mock
    return _call_next_stub


async def test_mark_request_session_add_uuid_to_request_state(request_mock, uuid_mock, call_next):
    await request.mark_request_session(request_mock, call_next)

    assert request_mock.state.id == uuid_mock.uuid4().hex


async def test_mark_request_session_set_request_context_var(request_mock, uuid_mock, call_next):
    with unittest.mock.patch('attack_surface_pypy.middlewares.request.context.request_id_var') as context_var_mock:
        await request.mark_request_session(request_mock, call_next)

    context_var_mock.set.assert_called_once_with(uuid_mock.uuid4().hex)


async def test_mark_request_session_set_request_id_header_to_response(
        request_mock, response_mock, uuid_mock, call_next
):
    await request.mark_request_session(request_mock, call_next)

    assert response_mock.headers == {constants.REQUEST_ID_HEADER_NAME: uuid_mock.uuid4().hex}


async def test_mark_request_session_returns_response_object(request_mock, response_mock, call_next):
    actual_result = await request.mark_request_session(request_mock, call_next)
    expected_result = response_mock

    assert expected_result is actual_result


@settings(suppress_health_check=(HealthCheck.function_scoped_fixture, ))
@given(
    first_call=st.floats(allow_nan=False, allow_infinity=False),
    second_call=st.floats(allow_nan=False, allow_infinity=False)
)
async def test_count_elapsed_time_set_time_into_request_state(request_mock, call_next, first_call, second_call):
    with unittest.mock.patch(
            'attack_surface_pypy.middlewares.request.time.perf_counter', side_effect=[first_call, second_call]
    ):
        await request.count_elapsed_time(request_mock, call_next)

    assert request_mock.state.elapsed_time_sec == second_call - first_call


@settings(suppress_health_check=(HealthCheck.function_scoped_fixture, ))
@given(
    first_call=st.floats(allow_nan=False, allow_infinity=False),
    second_call=st.floats(allow_nan=False, allow_infinity=False)
)
async def test_count_elapsed_time_writes_time_into_response_headers(
        request_mock, response_mock, call_next, first_call, second_call
):
    note('First call: %s, second call: %s' % (first_call, second_call))
    with unittest.mock.patch(
            'attack_surface_pypy.middlewares.request.time.perf_counter', side_effect=[first_call, second_call]
    ):
        await request.count_elapsed_time(request_mock, call_next)

    assert response_mock.headers == {constants.ELAPSED_TIME_HEADER_NAME: '%f' % (second_call - first_call)}


async def test_count_elapsed_time_returns_response_object(request_mock, response_mock, call_next):
    actual_result = await request.count_elapsed_time(request_mock, call_next)
    expected_result = response_mock

    assert expected_result is actual_result
