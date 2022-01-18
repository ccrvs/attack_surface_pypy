from attack_surface_pypy.core import exceptions


class InvalidFileDataError(exceptions.BaseError):
    _template = "Unable to parse data at %s"

    def __init__(self, message: str) -> None:
        super().__init__(self._template % message)
