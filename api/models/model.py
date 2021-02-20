from sqlalchemy.inspection import inspect

from ioc_fetch.app import db


class Model(db.Model):
    __abstract__ = True

    @classmethod
    def get_all(cls):
        return db.session.query(cls).all()

    @classmethod
    def get_by_id(cls, primary_key_id):
        kwargs = {
            inspect(cls).primary_key[0].name: primary_key_id
        }
        result = db.session.query(cls).filter_by(**kwargs)
        return result.first()

    def json(self):
        return dict((column.name, getattr(self, column.name))
                for column in self.__table__.columns)
