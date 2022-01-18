from attack_surface_pypy.core import exceptions


class VMNotFoundError(exceptions.BaseError):
    _template = "VM with the given id `{0!s}` is not found."

    def __init__(self, message: str) -> None:
        super().__init__(self._template.format(message))
