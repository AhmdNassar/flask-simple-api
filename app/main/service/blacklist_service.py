from app.main import db
from ..model.blacklist import BlacklistToken
import datetime


def save_token(token):
    blacklist_token = BlacklistToken(token=token,
                                     blacklisted_on=datetime.datetime.utcnow()
                                     )
    try:
        db.session.add(blacklist_token)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Successfully logged out.'
        }
        return response_object, 200

    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': str(e)
        }
        return response_object, 200
