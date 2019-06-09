from flask_restplus import Resource
from flask import request

from ..service.auth_helper import Auth
from ..utils.dto import AuthDto

api = AuthDto.api
_auth = AuthDto.user_auth


@api.route('/login')
class Login(Resource):
    @api.expect(_auth, validate=True)
    @api.doc("User login")
    @api.response(200, "Successfully logged in")
    def post(self):
        data = request.json
        return Auth.login(data)


@api.route('/logout')
class Logout(Resource):
    @api.doc("user logout")
    def post(self):
        auth_token = request.headers.get('Authorization')
        return Auth.logout(auth_token)
