from typing import Type

from flask import Flask
from flask_migrate import Migrate

from dh_backend.config import Config, DevelopmentConfig


class DhBackend(Flask):
    def __init__(self, name: str = "DhBackend", config: Type[Config] = DevelopmentConfig, *args, **kw):
        super(DhBackend, self).__init__(name, *args, **kw)

        self.config.from_object(config)

    def add_sqlalchemy(self):
        """ Create and configure SQLAlchemy extension """
        from dh_backend.models import db

        db.init_app(self)
        Migrate(self, db)


def create_app(*args, **kw):
    backend = DhBackend(*args, **kw)
    backend.add_sqlalchemy()
    return backend
