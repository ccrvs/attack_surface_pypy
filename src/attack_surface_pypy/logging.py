import collections
import logging
import traceback

import structlog

from attack_surface_pypy import settings, context


def filter_by_level(_, method_name, event_dict):
    method_level, settings_level = map(logging.getLevelName, (method_name.upper(), settings.log_level))
    if method_level < settings_level:
        raise structlog.DropEvent()
    return event_dict


def add_request_id(_, __, event_dict):
    request_id = context.request_id_var.get(None)
    if request_id:
        event_dict['request_id'] = request_id
    return event_dict


def format_traceback(_, __, event_dict):
    exc_info = event_dict.get('exc_info')
    if exc_info and not isinstance(exc_info, str):
        # unwrap tb to make it readable
        event_dict['exc_info'] = traceback.format_exception(*exc_info, limit=settings.traceback_depth)
        event_dict['tb_depth'] = settings.traceback_depth
    return event_dict


def format_error_messages(_, __, event_dict):
    record = event_dict['_record']
    message_level = record.levelno
    message_key = ('error', 'message')[message_level < logging.ERROR]  # probably it's not an error.
    event_dict[message_key] = record.msg  # TODO: shrink message?
    event_dict['event'] = record.name
    event_dict['pid'] = record.process
    event_dict['exc_info'] = record.exc_info or event_dict.get('exc_info')
    return event_dict


def format_access_to_json(_, __, event_dict):
    hypercorn_record = _unparse_hypercorn_log_message(event_dict['event'])
    logging_record = event_dict['_record']
    response_length = hypercorn_record.response_length
    if response_length == '-':
        response_length = 0
    event_dict['event'] = logging_record.name
    event_dict['pid'] = logging_record.process
    event_dict['remote_address'] = hypercorn_record.remote_address
    event_dict['elapsed_time_sec'] = int(hypercorn_record.request_time_microsec) / 1e6  # µsec to sec
    event_dict['protocol'] = float(hypercorn_record.protocol)
    event_dict['method'] = hypercorn_record.method
    event_dict['path'] = hypercorn_record.path_qs
    event_dict['status'] = int(hypercorn_record.status)
    event_dict['response_length'] = int(response_length)
    event_dict['referer'] = hypercorn_record.referer
    event_dict['user_agent'] = hypercorn_record.user_agent
    return event_dict


def _unparse_hypercorn_log_message(message):  # please, don't blame me
    LogStruct = collections.namedtuple('LogStruct', [
        'remote_address', 'request_time_microsec', 'protocol',
        'method', 'path_qs', 'status', 'response_length', 'referer', 'user_agent',
    ])
    delimiter = '#'
    return LogStruct(*message.split(delimiter))


def get_default_logging_config(log_level):
    pre_chain = [
        add_request_id,
        format_traceback,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(utc=True),
    ]

    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'json': {
                '()': structlog.stdlib.ProcessorFormatter,
                'processor': structlog.processors.JSONRenderer(),
                'foreign_pre_chain': pre_chain,
            },
            'error': {
                '()': structlog.stdlib.ProcessorFormatter,
                'processor': structlog.processors.JSONRenderer(),
                'foreign_pre_chain': [format_error_messages, *pre_chain]

            },
            'access': {
                '()': structlog.stdlib.ProcessorFormatter,
                'processor': structlog.processors.JSONRenderer(),
                'foreign_pre_chain': [format_access_to_json, *pre_chain],
            }
        },
        'handlers': {
            'std_json': {
                'level': log_level,
                'class': 'logging.StreamHandler',
                'formatter': 'json',
            },
            'std_error': {
                'level': log_level,
                'class': 'logging.StreamHandler',
                'formatter': 'error'
            },
            'std_access': {
                'level': log_level,
                'class': 'logging.StreamHandler',
                'formatter': 'access',
            }
        },
        'loggers': {
            '': {
                'handlers': ['std_json', ],
                'level': log_level,
                'propagate': True,
            },
            'hypercorn.access': {
                'handlers': ['std_access', ],
                'level': log_level,
                'propagate': False,
            },
            'hypercorn.error': {
                'handlers': ['std_error', ],
                'level': log_level,
                'propagate': False,
            }
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
        structlog.processors.UnicodeDecoder(encoding=settings.encoding),
        structlog.processors.TimeStamper(utc=True),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer(),
    ),
    wrapper_class=structlog.stdlib.BoundLogger,  # FIXME:
    context_class=structlog.threadlocal.wrap_dict(dict),
    # logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)
