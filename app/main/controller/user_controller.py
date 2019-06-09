from flask import request
from flask_restplus import Resource

from .. utils.dto import UserDto
from ..service.user_service import save_new_user, get_a_user, get_all_users
from app.main.utils.decorator import admin_token_required

api = UserDto.api
_user = UserDto.user


@api.route('/')
class UserList(Resource):
    @api.doc("list if registered users")
    @admin_token_required
    @api.marshal_list_with(_user, envelope='data')
    def get(self):
        """List of all registered users"""
        return get_all_users()

    @api.doc("add new user")
    @api.expect(_user, validate=True)
    @api.response(201, "user successfully created.")
    def post(self):
        data = request.json
        return save_new_user(data)


@api.route('/<public_id>')
@api.param('public_id', 'The User identifier')
@api.response(404, 'User not found.')
class User(Resource):
    @api.doc("get user with given id")
    @api.marshal_with(_user)
    def get(self, public_id):
        user = get_a_user(public_id)
        if user:
            print(user)
            return user
        else:
            api.abort(404)
