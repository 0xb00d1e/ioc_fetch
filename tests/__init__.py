import unittest

from ioc_fetch.app import create_app, db
from ioc_fetch.api.models import Role, User


class AppTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        try:
            self.create_test_user(db)
        except Exception:
            db.session.rollback()
            user = db.session.query(User).filter(User.username=='test').first()
            self.key = user.api_key

        self.client = self.app.test_client()

    def create_test_user(self, db):
        r1 = Role('admin')
        r2 = Role('user')
        db.session.add(r1)
        db.session.add(r2)
        db.session.commit()
        u = User('test', 'test', ['admin', 'user'])
        db.session.add(u)
        u.is_active = True
        self.key = u.api_key
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def http_status_code(self, resource):
        response = self.client.get(resource)
        return response.status_code

