import uuid
import datetime

from app.main import db
from app.main.model.user import User


def save_new_user(data):
    user = User.query.filter_by(email=data['email']).first()
    user_name = User.query.filter_by(username=data['username']).first()
    if not (user or user_name):
        new_user = User(
            public_id=str(uuid.uuid4()),
            email=data['email'],
            username=data['username'],
            password=data['password'],
            registered_on=datetime.datetime.utcnow(),
            admin=True if 'admin' in data and data['admin'] == "True" else False
        )
        try:
            save_changes(new_user)
        except Exception as e:
            response_object = {
                'status': 'fail',
                'message': "some thing goes worng, try again",
            }
            return response_object
        return generate_token(new_user)
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409


def get_all_users():
    return User.query.all()


def get_a_user(public_id):
    return User.query.filter_by(public_id=public_id).first()


def save_changes(data):

    db.session.add(data)
    db.session.commit()


def generate_token(user):
    try:
        auth_token = User.encode_auth_token(user.id)
        response_object = {
            'status': "success",
            'message': "successfully registered and logged in.",
            'Authorization': auth_token.decode()
        }
        return response_object, 201

    except Exception as e:
        print(e)
        response_object = {
            'status': "fail",
            'message': "Some error occurred. Please try again"
        }
        return response_object, 401
