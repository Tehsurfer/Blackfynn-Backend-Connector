# project/server/models.py


import jwt
import datetime
from blackfynn import Blackfynn

from project.server import app, db, bcrypt


class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    blackfynn_token = db.Column(db.String(255), nullable=True)
    blackfynn_secret = db.Column(db.String(255), nullable=True)
    blackfynn_session = db.Column(db.String(255), nullable=True)
    bf = db.Column(db.PickleType(), nullable=True)

    def __init__(self, email, password, admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()
        self.registered_on = datetime.datetime.now()
        self.admin = admin
        
    def add_blackfynn_tokens(self, blackfynn_session, blackfynn_token, blackfynn_secret):
        self.blackfynn_session = blackfynn_session
        self.blackfynn_token = blackfynn_token
        self.blackfynn_secret = blackfynn_secret
        
    def pickle_bf_object(self, bf):
        self.bf = bf
    

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=2, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            #is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            #if is_blacklisted_token:
            #    return 'Token blacklisted. Please log in again.'
            #else:
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def create_python_connection(self):
        bf = Blackfynn(api_token=self.blackfynn_token, api_secret=self.blackfynn_secret)
        print(bf)
        ds = bf.datasets()
        print(ds)


class BlacklistToken(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False
