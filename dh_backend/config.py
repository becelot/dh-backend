import os

from typing import Dict, Type


class Config:
    APP_NAME: str = 'dhistory'
    SECRET_KEY: str = 'dhistory'
    SQLALCHEMY_DATABASE_URI: str = 'undefined'
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = True
    DEBUG: bool = True


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI: str = 'postgresql://postgres@127.0.0.1:5432/devdb'
    LOG_FILE: str = 'backend.log'
    DEBUG = True


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI: str = 'postgresql://postgres@127.0.0.1:5432/testdb'
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI: str = os.environ.get('DATABASE_URL')
    SECRET_KEY: str = os.environ.get('SECRET_KEY')


config: Dict[str, Type[Config]] = {"dev": DevelopmentConfig, "prod": ProductionConfig, "test": TestConfig}
