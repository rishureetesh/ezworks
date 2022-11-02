from project import db
from sqlalchemy.dialects.mysql import INTEGER

class User(db.Model):
    __tablename__ = "EZ_users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, index=True)
    password = db.Column(db.Text, nullable=False)
    mobile = db.Column(db.BigInteger, unique=True, nullable=False, index=True)
    verification_slug = db.Column(db.String(255), nullable=False, index=True)
    verified = db.Column(db.Boolean, nullable=False)
    user_type = db.Column(db.Integer)


    def __init__(self, name, mobile, email, password, verification_slug, verified, user_type):
        self.name = name
        self.mobile = mobile
        self.email = email
        self.password = password
        self.verification_slug = verification_slug
        self.verified = verified
        self.user_type = user_type

    def create(self):
        db.session.add(self)
        db.session.commit()
        return 

class UserType(db.Model):
    __tablename__ = "EZ_user_types"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)


    def __init__(self, name):
        self.name = name

    def create(self):
        db.session.add(self)
        db.session.commit()
        return 