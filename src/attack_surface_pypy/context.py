import contextvars

request_id_var: contextvars.ContextVar[str] = contextvars.ContextVar("request_id")
# TODO: backpressure?
