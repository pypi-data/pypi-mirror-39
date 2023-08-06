import logging
import json

from logging.config import dictConfig
from pythonjsonlogger import jsonlogger
from flask import request as flask_request

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        
        if not log_record.get('request_id'):
            log_record['request_id'] = flask_request.headers['X-Request-Id'] if flask_request and \
                'X-Request-Id' in flask_request.headers else ''
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname

config = dict(
    version = 1,
    formatters = {
        'jsonformatter': {
            '()': CustomJsonFormatter,
            'format': '(level) (name) (message) (asctime) (request_id) (threadName)'
        },
    },
    handlers = {
        'stream': {
            '()': 'logging.StreamHandler',
            'formatter': 'jsonformatter',
            'level': logging.INFO
        }
    },
    root = {
        'handlers': ['stream'],
        'level': logging.INFO
    },
)

dictConfig(config)
