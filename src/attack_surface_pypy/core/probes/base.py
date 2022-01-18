class BaseProbe:
    def __init__(self, logging_factory, analytics_factory):
        self._logger = logging_factory()
        self._analytics = analytics_factory()
