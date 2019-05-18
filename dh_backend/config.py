import os

from typing import Dict, Type


class Config:
    APP_NAME: str = 'dhistory'
    SECRET_KEY: str = 'dhistory'
    SQLALCHEMY_DATABASE_URI: str = 'undefined'
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = True
    JWT_SECRET_KEY: str = 'geRgaDdHsi iK04hjFfDDsgEf Ldad Hearthstone'
    DEBUG: bool = True
    TWITCH_CLIENT_ID: str = '3jqh17gag0ubkiz9h24z7gp5x3fd8e'
    TWITCH_CLIENT_SECRET: str = os.environ.get('TWITCH_CLIENT_SECRET')


class DevelopmentConfig(Config):
    TWITCH_REDIRECT_URL: str = 'http://localhost:5000/api/auth/twitch_redirect'
    SQLALCHEMY_DATABASE_URI: str = 'postgresql://postgres@127.0.0.1:5432/devdb'
    LOG_FILE: str = 'backend.log'
    DEBUG = True


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI: str = 'postgresql://postgres@127.0.0.1:5432/testdb'
    TWITCH_REDIRECT_URL: str = 'http://localhost:5000/api/auth/twitch_redirect'
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI: str = os.environ.get('DATABASE_URL')
    SECRET_KEY: str = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY: str = os.environ.get('JWT_SECRET_KEY')


config: Dict[str, Type[Config]] = {"dev": DevelopmentConfig, "prod": ProductionConfig, "test": TestConfig}
