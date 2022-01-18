import statistics


class RouteAnalytics:
    def __init__(self):
        self._request_times = {}  # FIXME: fixed-size dict with rotation?
        self._response_times = {}

    def add_request_time(self, key, timestamp):
        self._request_times[key] = timestamp

    def add_response_time(self, key, timestamp):
        self._response_times[key] = timestamp

    def get_elapsed_time(self, key):
        return self._response_times[key] - self._request_times[key]

    def get_median_response_time(self):
        if not self._response_times:
            return None
        return statistics.median((self._response_times[k] - self._request_times[k] for k in self._response_times))
