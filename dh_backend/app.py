from typing import Type

from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from dh_backend.config import Config, DevelopmentConfig, TestConfig


class DhBackend(Flask):
    def __init__(self, name: str = "DhBackend", config: Type[Config] = DevelopmentConfig, *args, **kw):
        super(DhBackend, self).__init__(name, *args, **kw)

        self.config.from_object(config)

    def add_sqlalchemy(self):
        """ Create and configure SQLAlchemy extension """
        from dh_backend.models import db

        db.init_app(self)

    def add_restul_api(self) -> Api:
        """Registers the URL endpoints of the RESTful API"""
        from dh_backend.api import load_api

        return load_api(self)

    def add_logger(self):
        """Add a logger to the application"""
        from .logging import logger

        logger.init_app(self)

    def load_resources(self):
        """Load additional resources into memory"""
        from dh_backend.lib import hearthstone

        hearthstone.init_app(app=self)

    def add_auth(self):
        """Add authentication to application"""
        from flask_jwt_extended import JWTManager

        JWTManager(self)

    def add_twitch(self):
        """Add Twitch client to application"""
        from dh_backend.lib.twitch import twitch

        twitch.init_app(self)


def create_app(*args, **kw):
    backend = DhBackend(*args, **kw)
    backend.add_sqlalchemy()
    backend.add_logger()
    backend.add_restul_api()
    backend.load_resources()
    backend.add_auth()
    backend.add_twitch()
    CORS(backend)
    return backend


def create_migration_app(*args, **kw):
    backend = DhBackend(*args, **kw)
    backend.add_sqlalchemy()
    backend.add_logger()
    return backend


def create_test_app(*args, **kw):
    from tests.mock_endpoints import load_mock_endpoints

    backend = DhBackend(*args, config=TestConfig, **kw)
    backend.add_sqlalchemy()
    backend.add_logger()
    api: Api = backend.add_restul_api()
    load_mock_endpoints(api)
    backend.load_resources()
    backend.add_auth()
    backend.add_twitch()
    return backend
