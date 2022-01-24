import time
import typing
import uuid

import starlette.requests
import starlette.responses

from attack_surface_pypy import constants, context

T = typing.TypeVar('T', bound=starlette.responses.Response)


# it turned out that middlewares are extremely slow thus I've decided to shrink them as much as possible at least into
# a one middleware
async def mark_request_session_and_elapsed_time_sec(
        request: starlette.requests.Request,
        call_next: typing.Callable[..., typing.Awaitable[T]]
) -> T:
    request.state.id = request_id = uuid.uuid4().hex
    context.request_id_var.set(request_id)
    # started_at_sec = time.perf_counter()
    response = await call_next(request)
    # elapsed_sec = time.perf_counter() - started_at_sec
    # request.state.elapsed_time_sec = elapsed_sec
    # response.headers[constants.ELAPSED_TIME_HEADER_NAME] = '%f' % elapsed_sec
    response.headers[constants.REQUEST_ID_HEADER_NAME] = request_id
    return response
