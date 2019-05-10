import logging

from flask import request, has_request_context


class RequestFormatter(logging.Formatter):

    def __init__(self, fmt: str, fmt_fallback: str = None, *args, **kwargs):
        super(RequestFormatter, self).__init__(fmt, *args, **kwargs)
        self.fmt_fallback = logging.Formatter(fmt_fallback)

    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
            return super().format(record)
        else:
            return self.fmt_fallback.format(record)
