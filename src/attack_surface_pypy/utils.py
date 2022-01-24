import typing

import fastapi.exception_handlers
import fastapi.exceptions


async def validation_error_handler(request: typing.Any, exception: typing.Type[Exception]):
    if isinstance(exception, fastapi.exceptions.RequestValidationError):
        return await fastapi.exception_handlers.request_validation_exception_handler(request, exception)
