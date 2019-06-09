from ..model.user import User
from .blacklist_service import save_token


class Auth:

    @staticmethod
    def login(data):
        # get user form User
        try:
            user = User.query.filter_by(email=data.get('email')).first()
            if user:
                auth_token = User.encode_auth_token(user.id).decode()
                if auth_token:
                    response_opject = {
                        'status': "success",
                        'message': "Successfully logged in",
                        'Authorization': auth_token
                    }
                    return response_opject, 200

            else:
                response_opject = {
                    'status': "fail",
                    'message': "email or password does not match."
                }
                return response_opject, 401

        except Exception as e:
            print(e)
            response_object = {
                'status': 'fail',
                'message': 'Try again'
            }
            return response_object, 500

    @staticmethod
    def logout(auth_token):
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                return save_token(auth_token)

            else:
                response_object = {
                    'status': 'fail',
                    'message': str(resp)
                }

        else:
            response_object = {
                'status': "fail",
                "message": "Provide a valid auth token."
            }
        return response_object, 200

    @staticmethod
    def get_logged_in_user(new_request):
        # get the auth token
        auth_token = new_request.headers.get('Authorization')
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = User.query.filter_by(id=resp).first()
                response_object = {
                    'status': 'success',
                    'data': {
                        'user_id': user.id,
                        'email': user.email,
                        'admin': user.admin,
                        'registered_on': str(user.registered_on)
                    }
                }
                return response_object, 200
            response_object = {
                'status': 'fail',
                'message': str(resp)
            }
            return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            print("we are here")
            return response_object, 401
