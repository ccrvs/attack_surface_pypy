import typing

from attack_surface_pypy.core import exceptions


class TimeoutExceededError(exceptions.BaseError):
    _template = "The timeout has exceeded in %s seconds."

    def __init__(self, message: typing.Union[int, float]) -> None:
        super().__init__(self._template % message)
