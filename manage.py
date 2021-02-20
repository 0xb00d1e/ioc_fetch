import os
import sys
from getpass import getpass

import sqlalchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

sys.path.insert(0, '..')

from ioc_fetch.app import create_app, db
from ioc_fetch.api.models.role import Role
from ioc_fetch.api.models.user import User


app = create_app('prod')

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def seed():
    print('[*] Creating roles...')
    
    roles = ['admin', 'user']

    for role in roles:
        try:
            Role.create(role)
            print(f'[*] Created {role} role...')
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            print(f'[*] {role} role already exists')

    print('[*] Creating admin user...')

    user = db.session.query(User).filter(User.username=='admin').first()
    if not user:
        while True:
            password = getpass('[*] Enter new admin user password: ')
            password2 = getpass('[*] Enter password again: ')
            if password == password2:
                break
            print("[*] Passwords didn't match...")
        try:
            user = User.create('admin', password, roles)
            user.is_active = True
            db.session.commit()
            print('[*] admin user created')
        except sqlalchemy.exc.IntegrityError:
            print('[*] admin user already exists...')
    else:
        print('[*] admin user already exists...')


if __name__ == '__main__':
    manager.run()
