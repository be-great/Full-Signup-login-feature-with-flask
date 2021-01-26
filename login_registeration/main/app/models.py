from app import db ,app1
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class User(UserMixin,db.Model):
    __tablename__="User"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    email = db.Column(db.Text, nullable=False,unique=True)
    password = db.Column(db.Text, nullable=False) ## string(64)

    # it will be expire in 30 min
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app1.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token): ## it will return user object from id
        s = Serializer(app1.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

class Temporary_User(db.Model):
    __tablename__="Temporary_User"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    email = db.Column(db.Text, nullable=False,unique=True)
    password = db.Column(db.Text, nullable=False) ## string(64)


    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app1.config['SECRET_KEY'], expires_sec)
        return s.dumps({'Temporary_User_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token): ## it will return user object from id
        s = Serializer(app1.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['Temporary_User_id']
            print("+++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print(user_id,"  :")
            print("+++++++++++++++++++++++++++++++++++++++++++++++++++++")
        except:
            return None
        return Temporary_User.query.get(user_id)
