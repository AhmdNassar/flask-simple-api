import unittest
import datetime
import json

from app.main.controller.auth_controller import Login, Logout
from app.main.model.user import User
from app.main import db
from base import BaseTestCase


def register_user(self):
    return self.client.post(
        '/user/',
        data=json.dumps(dict(
            email='joe@gmail.com',
            username='username',
            password='123456'
        )),
        content_type='application/json'
    )


def login_user(self):
    return self.client.post(
        '/auth/login',
        data=json.dumps(dict(
            email='joe@gmail.com',
            password='123456'
        )),
        content_type='application/json'
    )


class TestAuthController(BaseTestCase):

    def test_registration(self):
        """Test register new user"""
        with self.client:
            resp = register_user(self)
            data = json.loads(resp.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'successfully registered and logged in.')
            self.assertTrue(data['Authorization'])
            self.assertEqual(resp.status_code, 201)

    def test_registration_with_exist_user(self):
        """Test register with already exist user"""
        register_user(self)  # register user
        with self.client:
            resp = register_user(self)
            data = json.loads(resp.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'User already exists. Please Log in.')
            self.assertEqual(resp.status_code, 409)

    def test_login_with_exist_user(self):
        """Test log in with exist user in DB"""
        register_user(self)
        with self.client:
            resp = login_user(self)
            data = json.loads(resp.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in')
            self.assertTrue(data['Authorization'])
            self.assertEqual(resp.status_code, 200)

    def test_login_with_notexist_user(self):
        """Test loging with none registered user"""
        with self.client:
            resp = login_user(self)
            data = json.loads(resp.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'email or password does not match.')
            self.assertEqual(resp.status_code, 401)

    def test_valid_logout(self):
        register_user(self)
        with self.client:
            resp = login_user(self)
            data = json.loads(resp.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged in')
            self.assertTrue(data['Authorization'])
            self.assertEqual(resp.status_code, 200)
            resp = self.client.post(
                '/auth/logout',
                headers=dict(Authorization=data['Authorization'])
            )
            data = json.loads(resp.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged out.')
            self.assertEqual(resp.status_code, 200)


if __name__ == "__main__":
    unittest.run()
