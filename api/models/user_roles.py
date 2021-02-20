from ioc_fetch.app import db
from ioc_fetch.api.models.model import Model


class UserRoles(Model):
    __tablename__ = 'user_roles'
    
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True)
