import os

from ioc_fetch.lib.util import get_env_db_url


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'nid89qhg3uiqdbgvyudf7823gdv9oi'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    USER_ENABLE_EMAIL = False
    APP_URL = ''


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = get_env_db_url('prod')


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = get_env_db_url('test')


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = get_env_db_url('dev')
