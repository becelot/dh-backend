from typing import Type

from flask import Flask

from dh_backend.config import Config, DevelopmentConfig


class DhBackend(Flask):
    def __init__(self, name: str = "DhBackend", config: Type[Config] = DevelopmentConfig, *args, **kw):
        super(DhBackend, self).__init__(name, *args, **kw)

        self.config.from_object(config)


def create_app(*args, **kw):
    backend = DhBackend(*args, **kw)
    return backend
