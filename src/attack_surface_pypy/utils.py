__all__ = (
    'validation_error_handler',
    'orjson_dumps',
)

import typing

import fastapi.exception_handlers
import fastapi.exceptions
import orjson


async def validation_error_handler(request: typing.Any, exception: typing.Type[Exception]):
    if isinstance(exception, fastapi.exceptions.RequestValidationError):
        return await fastapi.exception_handlers.request_validation_exception_handler(request, exception)


def orjson_dumps(v: typing.Any, *, default: typing.Any) -> str:
    return orjson.dumps(v, default=default).decode('utf-8')
