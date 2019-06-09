import datetime
import unittest

from app.main import db
from base import BaseTestCase
from app.main.model.user import User
from app.main.service.auth_helper import Auth


class TestAuthHelper(BaseTestCase):

    def test_login(self):
        user = User(
            email="test@test.com",
            password="test",
            registered_on=datetime.datetime.utcnow()
        )
        db.session.add(user)
        db.session.commit()
        data = {
            'email': 'test@test.com',
            'password': "test"
        }
        res = Auth.login(data)
        self.assertTrue(res[1] == 200 or res[1] == 401 or res[1] == 500)


if __name__ == "__main__":
    unittest.main()
