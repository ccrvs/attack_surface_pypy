class BaseError(Exception):
    ...


class InternalError(BaseError):
    _default = "An internal error has occurred."

    def __init__(self):
        super().__init__(self._default)
