import unittest
import datetime


from app.main import db
from base import BaseTestCase
from app.main.model.user import User


class TestUserModel(BaseTestCase):

    def test_encode_auth_token(self):
        user = User(
            email="test@test.com",
            registered_on=datetime.datetime.utcnow(),
            password="test"
        )

        db.session.add(user)
        db.session.commit()
        auth_token = User.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user = User(
            email="test@test.com",
            registered_on=datetime.datetime.utcnow(),
            password="test"
        )
        db.session.add(user)
        db.session.commit()
        auth_token = User.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(User.decode_auth_token(auth_token) == 1)


if __name__ == "__main__":
    unittest.main()
