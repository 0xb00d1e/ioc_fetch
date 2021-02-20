import os
from datetime import date

from flask.json import JSONEncoder


def get_env_db_url(env_setting):
    if env_setting == 'dev':
        DB_USER = get_env_variable('DEV_DB_USER')
        DB_PW = get_env_variable('DEV_DB_PW')
        DB_HOST = get_env_variable('DEV_DB_HOST')
        DB_DB = get_env_variable('DEV_DB_DB')
    elif env_setting == 'test':
        DB_USER = get_env_variable('TEST_DB_USER')
        DB_PW = get_env_variable('TEST_DB_PW')
        DB_HOST = get_env_variable('TEST_DB_HOST')
        DB_DB = get_env_variable('TEST_DB_DB')
    elif env_setting == 'prod':
        DB_USER = get_env_variable('PROD_DB_USER')
        DB_PW = get_env_variable('PROD_DB_PW')
        DB_HOST = get_env_variable('PROD_DB_HOST')
        DB_DB = get_env_variable('PROD_DB_DB')

    return create_db_url(DB_USER, DB_PW, DB_HOST, DB_DB)


def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        message = f'Expected environment variable "{name}" not set.'
        raise Exception(message)


def create_db_url(user, pw, url, db):
    return f'postgresql://{user}:{pw}@{url}/{db}'


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)
