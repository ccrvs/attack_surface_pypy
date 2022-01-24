__all__ = (
    'structlog',
    'get_default_logging_config',
)

import logging.handlers
import queue
import traceback

import orjson
import structlog

from attack_surface_pypy import context, settings

# logging_queue = queue.Queue(-1)
# queue_handler = logging.handlers.QueueHandler(logging_queue)
# handler = logging.StreamHandler()
# listener = logging.handlers.QueueListener(logging_queue, handler)


def filter_by_level(_logger, method_name, event_dict):
    method_level, settings_level = map(logging.getLevelName, (method_name.upper(), settings.log_level))
    if method_level < settings_level:
        raise structlog.DropEvent()
    return event_dict


def add_request_id(_logger, _method_name, event_dict):
    request_id = context.request_id_var.get(None)
    if request_id:
        event_dict['request_id'] = request_id
    return event_dict


def format_traceback(_logger, _method_name, event_dict):
    exc_info = event_dict.get('exc_info')
    if exc_info and not isinstance(exc_info, str):
        # unwrap tb to make it readable
        event_dict['exc_info'] = traceback.format_exception(*exc_info, limit=settings.traceback_depth)
        event_dict['tb_depth'] = settings.traceback_depth
    return event_dict


def format_error_messages(_logger, _method_name, event_dict):
    record = event_dict['_record']
    message_level = record.levelno
    message_key = ('error', 'message')[message_level < logging.ERROR]  # probably it's not an error.
    event_dict[message_key] = record.msg  # TODO: shrink message?
    event_dict['event'] = record.name
    event_dict['pid'] = record.process
    event_dict['exc_info'] = record.exc_info or event_dict.get('exc_info')
    return event_dict


def get_default_logging_config(log_level):
    pre_chain = [
        add_request_id,
        format_traceback,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(utc=True),
    ]

    return {
        'version': 1,
        'level': log_level,
        'disable_existing_loggers': False,
        'formatters': {
            'json': {
                '()': structlog.stdlib.ProcessorFormatter,
                'processor': structlog.processors.JSONRenderer(),
                'foreign_pre_chain': pre_chain,
            },
        },
        'handlers': {
            'std_json': {
                # '()': lambda: queue_handler,
                'level': log_level,
                'formatter': 'json',
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            '': {
                'handlers': ['std_json', ],
                'level': log_level,
                'propagate': True,
            },
        }
    }


structlog.configure(
    processors=(
        filter_by_level,
        add_request_id,
        format_traceback,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.format_exc_info,
        structlog.stdlib.add_log_level,
        # TODO: sentry
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(utc=True),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer(serializer=orjson.dumps),
    ),
    wrapper_class=structlog.make_filtering_bound_logger(logging.getLevelName(settings.log_level)),
    context_class=dict,
    logger_factory=structlog.BytesLoggerFactory(),
    cache_logger_on_first_use=True,
)
