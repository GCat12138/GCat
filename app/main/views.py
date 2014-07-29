from .. import db
from ..models import User, Address, ActualMeal, Meal, Picture, Order
from flask import render_template, request, redirect, url_for
from . import main
from forms import UserForm, LoginForm
from flask.ext.login import current_user, login_user, logout_user,\
        login_required
import flask
import datetime, time

@main.before_app_request
def before_request():
    pass

@main.route('/', methods=['GET'])
@main.route('/index', methods=['GET'])
def index():
    today_date = datetime.date.today()
    current_datetime = datetime.datetime.now()
    current_time = datetime.time(
               current_datetime.hour,
               current_datetime.minute
            )

    if current_user.is_authenticated():
        addressID = current_user.addressId

        current_actualMeal = ActualMeal.query.filter(
                ActualMeal.addressId == addressID,
                ActualMeal.date == today_date,
                ActualMeal.time > current_time).first()
    else:
        current_actualMeal = ActualMeal.query.filter(
                ActualMeal.date == today_date,
                ActualMeal.time > current_time
            ).limit(1).all()
        if len( current_actualMeal ) > 0:
            current_actualMeal = current_actualMeal[0]
        else:
            current_actualMeal = None

#    calculate the duration between the start time of the next meal
#    and current time
    duration = (
    datetime.datetime.combine(datetime.date.today(), current_actualMeal.time) -
    datetime.datetime.combine(datetime.date.today(), current_time)
    ).total_seconds()

    print duration
    print (
    datetime.datetime.combine(datetime.date.today(), current_actualMeal.time) -
    datetime.datetime.combine(datetime.date.today(), current_time)
    )

    #form of login
    loginForm = LoginForm()
    userForm = UserForm()
    # set the choices of register form(user form)
    userForm.addresses.choices = [
            (address.id, address.address) for address in Address.query.all()
        ]
    HiddenRegisterForm = UserForm()
    # set the choices
    HiddenRegisterForm.addresses.choices = [
            (address.id, address.address) for address in Address.query.all()
        ]
    if current_actualMeal:
        mealInformation = Meal.query.get( int(current_actualMeal.mealID) )
        mainPicture = Picture.query.filter_by(
            mealId = mealInformation.id, type=0).first()

        mealPicture = Picture.query.filter_by(
            mealId = mealInformation.id, type=1).all()

        materialPicture = Picture.query.filter_by(
            mealId = mealInformation.id, type=2).all()

    else:
        mealInformation = None
        mainPicture = None
    if mealInformation:
        return render_template('main.html',
                userForm = userForm,
                loginForm = loginForm,
                meal = mealInformation,
                ameal = current_actualMeal,
                mainPict = mainPicture,
                mealPics = mealPicture,
                materialPics = materialPicture,
                hidden_register_form = HiddenRegisterForm,
                duration = duration
                )
    else:
        return "No Meal Today"

@main.route('/register', methods=['POST'])
def register():
    print request.form
    userForm = UserForm(request.form)
    userForm.addresses.choices = [
            (address.id, address.address) for address in Address.query.all()
        ]
    if userForm.validate_on_submit():
        phoneNumber = userForm.phoneNumber.data
        nickName = userForm.nickName.data
        addressID = userForm.addresses.data
        password = userForm.password.data
        newUser = User(phoneNumber, nickName, password, addressID)
        db.session.add(newUser)
        try:
            db.session.commit()
        except Exception as e:
            print e
            db.session.rollback()
        return 'success'
    else:
        print userForm.errors
        return 'failed'

@main.route('/login', methods=['POST'])
def logIn():
    print dir(request)
    loginForm = LoginForm(request.form)
    if loginForm.validate_on_submit():
        user = User.query.filter_by(phoneNumber = loginForm.phoneNumber.data).first()
        if user is not None and user.verify_password(loginForm.password.data):
            login_user(user, remember = True)
            print "log in success"
            return '1'
        else:
            print 'no such user'
            return '0'
    else:
        print loginForm.errors
        return '0'

@main.route('/logout')
@login_required
def LogOut():
    logout_user()
    return redirect( url_for('main.index') )

@main.route('/like', methods=['POST'])
def Like():
    mealId = request.form['mealId']
    meal = Meal.query.get( int(mealId) )
    meal.likes = meal.likes + 1
    newLikes = meal.likes
    try:
        db.session.add(meal)
        db.session.commit()
    except Exception as e:
        print e
        return "failed"

    return str(newLikes)
    pass

def MakeOrderHelperFunction():
    newOrder = Order()
    Ameal = ActualMeal.query.get( int( request.form['amealId']) )
    tempAvailableNumber = 0
    try:
        Ameal.availableNumber = Ameal.availableNumber - 1
        db.session.add( Ameal )
        db.session.commit()
        tempAvailableNumber = Ameal.availableNumber
    except Exception as e:
        print e
        db.session.rollback()
        print "failed to make order"
        return '0'

    newOrder.userID = current_user.id
    newOrder.mealId = Ameal.mealID
    newOrder.number = Ameal.amount - tempAvailableNumber
    newOrder.date = datetime.date.today()
    current_time = datetime.datetime.now()

    newOrder.time = datetime.time(
            current_time.hour,
            current_time.minute
    )
    try:
        db.session.add( newOrder )
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print e
        Ameal.availableNumber = Ameal.availableNumber + 1
        db.session.add( Ameal )
        db.session.commit()
        print "failed to make order"
        return '0'
    return '1'

@main.route('/make_order', methods=['POST'])
def MakeOrder():
    print request.form
    if current_user.is_authenticated():
        #check the password
       if logIn() == '1':
           result = MakeOrderHelperFunction()
           return result
           pass
    else:
        registerForm = LoginForm( request.form )
        if logIn() == '1':
#           This user has already registered, but did not log in
#           Make the order
            pass
        else:
#           This is a new user, add the user to the database

#           Make the order
            pass
        pass
    pass

@main.route('/test', methods=['POST', 'GET'])
def test():
    a = Address()
    return 'ggg'
