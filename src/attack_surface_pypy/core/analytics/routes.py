""" Module with the analytics components, related to api routes.

RouteAnalytics -- a component with base routes analytics.
"""

__all__ = ("RouteAnalytics", )

import collections
import contextlib
import statistics
import time
import typing


class RouteAnalytics:
    _TRACING_DEPTH = 100  # TODO: update docstring according to changes
    """ Routes analytics class provides the minimum required analytics methods necessary for time consumption tracking.

    At most naive realization it should be treated as a utility object, no advanced logic is required. The class
    is injected at a probe initialization step and lives within it during a  process lifespan.

    Example:
        >>> analytics = RouteAnalytics()
        >>> analytics.add_request_time('some_key', 26943.769990649)  # mark the request has started
        >>> analytics.add_response_time('some_key', 26966.634195516)  # mark the request has ended
        >>> analytics.get_elapsed_time('some_key')
        22.86420486699717
        >>> analytics.get_requests_count()
        1
    """

    def __init__(self) -> None:
        self._requests_count: int = 0
        self._elapsed_times: typing.Deque[float] = collections.deque(maxlen=self._TRACING_DEPTH)

    @contextlib.contextmanager
    def trace_request(self) -> typing.Iterator[None]:
        started_at = time.perf_counter()
        try:
            yield
        finally:
            self._requests_count += 1
            self._elapsed_times.append(time.perf_counter() - started_at)

    def register_request(self) -> None:
        self._requests_count += 1

    def register_elapsed_time(self, elapsed_time: float) -> None:
        self._elapsed_times.append(elapsed_time)

    def get_requests_count(self) -> int:
        """
        Counts a number of the processed requests.
        :return: number of requests.
        """
        return self._requests_count

    def get_median_response_time(self) -> typing.Optional[float]:
        """
        Calculates a median response time among all the processed requests via statistics module.
        :return: a median response time or nothing, if no responses have been processed yet.
        """
        if self._elapsed_times:
            return statistics.median(self._elapsed_times)
        return None

    def get_mean_response_time(self) -> typing.Optional[float]:
        """
        Calculates an average response time among all the processed requests via statistics module.
        :return: an average response time or nothing, if no responses have been processed yet.
        """
        if self._elapsed_times:
            return statistics.fmean(self._elapsed_times)
        return None
