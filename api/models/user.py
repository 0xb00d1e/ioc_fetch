import secrets
import string
from datetime import datetime

from flask_user import UserMixin
from werkzeug.security import generate_password_hash

from ioc_fetch.app import db
from ioc_fetch.api.models.model import Model
from ioc_fetch.api.models.role import Role


class User(Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    is_active = db.Column(db.Boolean, nullable=False, server_default='0')
    created = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    api_key = db.Column(db.Text, nullable=False, unique=True)

    roles = db.relationship('Role', secondary='user_roles')

    def __init__(self, username, password, role_names):
        self.username = username
        self.password = generate_password_hash(password)
        self.api_key = self.generate_api_key()

        for role in Role.get_by_names(role_names):
            self.roles.append(role)

    @classmethod
    def create(cls, username, password, role_names):
        new_user = cls(username, password, role_names)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @classmethod
    def get_user_by_apikey(cls, api_key): 
        return db.session.query(cls).filter((cls.api_key == api_key)).first()

    def role_names(self):
        return [role.name for role in self.roles]

    def generate_api_key(self):
        return ''.join(secrets.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits)
                    for _ in range(64))

    def json(self):
        result = {}
        for column in self.__table__.columns:
            if column.name == 'password':
                continue
            result[column.name] = getattr(self, column.name)
        result['role_names'] = [r.name for r in self.roles]
        return result
