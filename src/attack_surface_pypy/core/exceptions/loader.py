import pathlib
import typing

from attack_surface_pypy.core.exceptions import base


class LoaderFileNotFoundError(base.BaseError):
    _template = "No such file or directory: `{0!s}`"

    def __init__(self, message: typing.Union[str, pathlib.Path]) -> None:
        super().__init__(self._template.format(message))
