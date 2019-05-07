import logging

from flask import Flask

from dh_backend.logging.formatter import RequestFormatter


class Logger(object):

    def init_app(self, app: Flask):
        formatter = RequestFormatter(
            "%(asctime)s %(remote_addr)s: requested %(url)s: %(levelname)s in [%(module)s: %(lineno)d]: %(message)s"
        )
        if app.config.get("LOG_FILE"):
            fh = logging.FileHandler(app.config.get("LOG_FILE"))
            fh.setLevel(logging.INFO)
            fh.setFormatter(formatter)
            app.logger.addHandler(fh)

        strm = logging.StreamHandler()
        strm.setLevel(logging.INFO)
        strm.setFormatter(formatter)

        app.logger.addHandler(strm)
        app.logger.setLevel(logging.INFO)
