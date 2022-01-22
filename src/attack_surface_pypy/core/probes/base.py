""" Base probes module.

BaseProbe -- a predecessor for all the probes created.
"""

__all__ = (
    'BaseProbe',
)

import structlog


class BaseProbe:
    """
    The probe is an attempt to implement domain-oriented observability.

    Each probe is responsible for handling log messages, analytics, and metrics processing, binding them not just
    to abstract events but to get together them within specific domain events.
    """
    __slots__ = ('_analytics', )
    _logger = structlog.get_logger()

    def __init__(self, analytics_factory):
        self._analytics = analytics_factory()

    @property
    def analytics(self):
        return self._analytics
