from typing import Type

from flask import Flask

from dh_backend.config import Config, DevelopmentConfig, TestConfig


class DhBackend(Flask):
    def __init__(self, name: str = "DhBackend", config: Type[Config] = DevelopmentConfig, *args, **kw):
        super(DhBackend, self).__init__(name, *args, **kw)

        self.config.from_object(config)

    def add_sqlalchemy(self):
        """ Create and configure SQLAlchemy extension """
        from dh_backend.models import db

        db.init_app(self)

    def add_logger(self):
        from .logging import logger

        logger.init_app(self)


def create_app(*args, **kw):
    backend = DhBackend(*args, **kw)
    backend.add_sqlalchemy()
    backend.add_logger()
    return backend


def create_test_app():
    return create_app(config=TestConfig)
