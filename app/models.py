from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask.ext.login import UserMixin
from . import login_manager

class Address(db.Model):
    __tablename__ = 'address'

    id = db.Column(db.Integer, primary_key = True)
    address = db.Column(db.String(64), unique = True, index = True)


    def __init__(self, address):
        self.address = address

    def __repr__(self):
        return '<Address is %r>' % self.address
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True, unique = True)
    phoneNumber = db.Column(db.String(11),
            unique = True,
            index = True,
            nullable = False)
    nickName = db.Column(db.String(12))
    #salted password
    password_hash = db.Column(db.String(128))
    #Foreign Key, address_id
    addressId = db.Column(db.Integer, db.ForeignKey('address.id', ondelete="SET NULL"))

    def __init__(self,
            phoneNumber=None,
            nickName=None,
            password=None,
            addressId=None):
        self.phoneNumber = phoneNumber
        self.nickName = nickName
        self.password = password
        self.addressId = addressId

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        #self.password_hash = password

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    def __repr__(self):
        return '<User is %r>' % self.nickName

class Meal(db.Model):
    __tablename__ = 'meals'
    id = db.Column(db.Integer, primary_key = True, unique = True)

    description = db.Column(db.String(64))
    price = db.Column(db.Float, nullable = False)
    discount = db.Column(db.Float, default = 0.0)
    likes = db.relationship("LikeModel", backref="meals")
#    amount = db.Column(db.Integer, default = 0)
#    availableNumber = db.Column(db.Integer, default = 0)

    def __repr__(self):
        return '<meal is %r>' % self.description

class LikeModel(db.Model):
    __tablename__ = "likes"

    id = db.Column(db.Integer, primary_key = True)
    mealID = db.Column(db.Integer, db.ForeignKey('meals.id', ondelete="CASCADE"))
    userID = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))

class Picture(db.Model):
    __tablename__ = 'pictures'

    id = db.Column(db.Integer, primary_key = True)
    type = db.Column(db.SmallInteger, nullable = False)
    name = db.Column(db.String(32))
    description = db.Column(db.String(64))
    mealId = db.Column(db.Integer, db.ForeignKey('meals.id', ondelete="SET NULL"))

    def __repr__(self):
        return '<Picture Url: %r>' % self.url

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key = True)
    number = db.Column(db.Integer, nullable = False)
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    userID = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))
    amealId = db.Column(db.Integer, db.ForeignKey('actualmeals.id', ondelete="SET NULL"))

    def __repr__(self):
        return '<Order id is %r>' % self.id

class ActualMeal(db.Model):
    __tablename__ = 'actualmeals'

    id = db.Column(db.Integer, primary_key = True)
    amount = db.Column(db.Integer, default = 0)
    availableNumber = db.Column(db.Integer, default = 0)
    date = db.Column(db.Date)
    startTime = db.Column(db.Time)
    endTime = db.Column(db.Time)
    mealID = db.Column(
            db.Integer,
            db.ForeignKey('meals.id', ondelete="CASCADE"),
            unique = False)

    addressId = db.Column(
            db.Integer,
            db.ForeignKey('address.id', ondelete="CASCADE")
            )

class SMSModel(db.Model):
    __tablename__ = 'sms'

    id = db.Column(db.Integer, primary_key = True)
    number = db.Column(db.Integer, nullable = False)
    phoneNumber = db.Column(db.String(11), nullable = False, unique = False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get( int(user_id) )
