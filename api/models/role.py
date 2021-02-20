from ioc_fetch.app import db
from ioc_fetch.api.models.model import Model


class Role(Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.Text, unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    @classmethod
    def create(cls, name):
        new_role = cls(name)
        db.session.add(new_role)
        db.session.commit()
        return new_role

    @classmethod
    def get_by_name(cls, name):
        result = db.session.query(cls).filter(cls.name==name).first()
        return result

    @classmethod
    def get_by_names(cls, names):
        roles = []
        for name in names:
            role = db.session.query(cls).filter((cls.name == name)).first()
            roles.append(role)
        return roles
