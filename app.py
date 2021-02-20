import sys
from pathlib import Path

sys.path.insert(0, '..')

from dotenv import load_dotenv
from flask import Flask
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

#from extensions import db
#from lib.util import CustomJSONEncoder
from ioc_fetch.extensions import db
from ioc_fetch.lib.util import CustomJSONEncoder


def create_app(environment):
    app = Flask(
        __name__,
        instance_relative_config=True
    )

    load_env_vars(Path(__file__).resolve().parent)
    configure_app(app, environment)
    configure_extensions(app)
    configure_addons(app)
    configure_blueprints(app)
    return app


def configure_app(app, environment):
    app.url_map.strict_slashes = False
    if environment == 'test':
        app.config.from_object('ioc_fetch.config.TestConfig')
    elif environment == 'dev':
        app.config.from_object('ioc_fetch.config.DevConfig')
    elif environment == 'prod':
        app.config.from_object('ioc_fetch.config.ProdConfig')


def load_env_vars(path):
    env_vars = Path(path) / '.env'
    load_dotenv(dotenv_path=env_vars)


def configure_addons(app):
    app.json_encoder = CustomJSONEncoder


def configure_blueprints(app):
    from ioc_fetch.api import api

    bps = [api]

    for bp in bps:
        app.register_blueprint(bp)


def configure_extensions(app):
    db.init_app(app)


def migrations(app, db):
    migrate = Migrate(app, db)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    manager.run()


if __name__ == '__main__':
    app = create_app('dev')
    app.run(host='0.0.0.0', port=8080, debug=True)
