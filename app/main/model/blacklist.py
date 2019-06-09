from .. import db


class BlacklistToken(db.Model):
    """
    Token model for storing JWT tokens
    """

    __tablename__ = "blacklist_tokens"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(250), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"token {self.token}"

    @staticmethod
    def check_blacklist(token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(token)).first()
        if res:
            return True
        return False
