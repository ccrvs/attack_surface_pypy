import time

from attack_surface_pypy.core.probes import base


class RouteProbe(base.BaseProbe):

    def request(self, path, request_id):
        self._analytics.add_request_time(request_id, time.perf_counter())
        self._logger.info('router.request', path=path, request_id=request_id)

    def response(self, path, request_id, status_code):
        self._analytics.add_response_time(request_id, time.perf_counter())
        self._logger.info(
            'router.response',
            path=path,
            request_id=request_id,
            elapsed_sec=self._analytics.get_elapsed_time(request_id),
            status_code=status_code,
            median_time=self._analytics.get_median_response_time(),
        )

    def error(self, path, error, status_code):
        self._logger.error('router.error', path=path, error=error, status_code=status_code)

    def not_found(self, path, **kwargs):
        self._logger.warning('router.not_found', path=path, **kwargs)
