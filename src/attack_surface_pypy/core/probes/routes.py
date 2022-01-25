import contextlib
import time

import structlog

from attack_surface_pypy.core.probes import base

logger = structlog.get_logger()


# TODO: maybe better to create context for each request and manipulate all the activities within them?
#  ctx.request, stx.response, cts.get_elapsed_time
class RouteProbe(base.BaseProbe):

    @contextlib.contextmanager
    def trace_request(self, request_id):
        self._analytics.register_request()
        self.request(request_id)
        started_at = time.perf_counter()
        try:
            yield
        finally:
            elapsed_time_sec = time.perf_counter() - started_at
            self._analytics.register_elapsed_time(elapsed_time_sec)
            self.response(request_id, elapsed_time_sec)

    def request(self, request_id):
        # self._analytics.add_request_time(request_id, time.perf_counter())

        logger.info("router.request", request_id=request_id)

    def response(self, request_id, elapsed_time_sec):
        # self._analytics.add_response_time(request_id, time.perf_counter())
        logger.info("router.response", request_id=request_id, elapsed_time_sec=elapsed_time_sec)

    def error(self, path, error, status_code):
        logger.error("router.error", path=path, error=error, status_code=status_code)

    def not_found(self, path, **kwargs):
        logger.warning("router.not_found", path=path, **kwargs)
