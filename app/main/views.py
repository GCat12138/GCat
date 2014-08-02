# coding=utf8
from .. import db
from ..models import User, Address, ActualMeal, Meal, Picture, Order, SMSModel
from flask import render_template, request, redirect, url_for
from . import main
from forms import UserForm, LoginForm, SMSForm
from flask.ext.login import current_user, login_user, logout_user,\
        login_required
import flask
import datetime, time
from sqlalchemy import and_, or_
import json
import urllib2
from ..shareVars import SMS_URL
from xml.dom import minidom
import random


@main.before_app_request
def before_request():
    pass

def Duration_between_times( time1, time2):
    date1 = datetime.datetime.combine(
                datetime.date.today(),
                time1
            )
    date2 = datetime.datetime.combine(
                datetime.date.today(),
                time2
            )
    return (date1 - date2).total_seconds()

@main.route('/', methods=['GET'])
@main.route('/index', methods=['GET'])
def index():
    today_date = datetime.date.today()
    current_datetime = datetime.datetime.now()
    current_time = datetime.time(
               current_datetime.hour,
               current_datetime.minute
            )

# select meal from database
    if current_user.is_authenticated():
        addressID = current_user.addressId

        current_actualMeal = ActualMeal.query.filter(
                ActualMeal.addressId == addressID,
                ActualMeal.date == today_date).filter(
                    or_(
                        ActualMeal.startTime > current_time,
                        and_(
                            ActualMeal.startTime<= current_time,
                            ActualMeal.endTime >= current_time
                        )
                    )
                ).order_by(ActualMeal.startTime).first()
    else:

        current_actualMeal = ActualMeal.query.filter(
                ActualMeal.date == today_date
            ).filter(
                or_(ActualMeal.startTime >= current_time,
                        and_(ActualMeal.startTime <= current_time,  ActualMeal.endTime >= current_time))
                        ).limit(1).all()


        if len( current_actualMeal ) > 0:
            current_actualMeal = current_actualMeal[0]
        else:
            current_actualMeal = None


    #form of login
    loginForm = LoginForm(request.form)

    # form of register
    userForm = UserForm(request.form)
    # set the choices of register form(user form)
    userForm.addresses.choices = [
            (address.id, address.address) for address in Address.query.all()
        ]
    HiddenRegisterForm = UserForm(request.form)
    # set the choices
    HiddenRegisterForm.addresses.choices = [
            (address.id, address.address) for address in Address.query.all()
        ]
    if current_actualMeal:
#    calculate the duration between the start time of the next meal
#    and current time
        startDuration = Duration_between_times(
                    current_actualMeal.startTime,
                    current_time
                )
        endDuration = Duration_between_times(
                    current_actualMeal.endTime,
                    current_time
                )

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
                startDuration = startDuration,
                endDuration = endDuration,
                sForm = SMSForm()
                )
    else:
        return "No Meal Today"

def register_helper_function():
    userForm = UserForm(request.form)
    userForm.addresses.choices = [
            (address.id, address.address) for address in Address.query.all()
        ]
    if userForm.validate_on_submit():
        verificaion_code = userForm.verification.data
        phoneNumber = userForm.phoneNumber.data

        sms_code = SMSModel.query.filter_by(phoneNumber = phoneNumber).first()
        if sms_code.number !=  int(verificaion_code):
            # verification code is incorrect
            return "2"

        nickName = userForm.nickName.data
        addressID = userForm.addresses.data
        password = userForm.password.data
        newUser = User(phoneNumber, nickName, password, addressID)
        db.session.add(newUser)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print e
            return "0"

        # log the uesr in
        user = User.query.filter_by(phoneNumber = phoneNumber).first()
        if user is None:
            return '0'
        else:
            login_user(user, remember = True)
            try:
                db.session.delete( sms_code )
                db.session.commit()
            except:
                db.rollback()
        return '1'
    else:
        print userForm.errors
        return '0'


@main.route('/register', methods=['POST'])
def register():
    userForm = UserForm(request.form)
    userForm.addresses.choices = [
            (address.id, address.address) for address in Address.query.all()
        ]
    if userForm.validate_on_submit():
        verificaion_code = userForm.verification.data
        phoneNumber = userForm.phoneNumber.data

        sms_code = SMSModel.query.filter_by(phoneNumber = phoneNumber).first()
        if sms_code.number !=  int(verificaion_code):
            # verification code is incorrect
            return "2"

        nickName = userForm.nickName.data
        addressID = userForm.addresses.data
        password = userForm.password.data
        newUser = User(phoneNumber, nickName, password, addressID)
        db.session.add(newUser)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print e
            return "0"

        # log the uesr in
        user = User.query.filter_by(phoneNumber = phoneNumber).first()
        if user is None:
            return '0'
        else:
            login_user(user, remember = True)
            try:
                db.session.delete( sms_code )
                db.session.commit()
            except:
                db.rollback()
        return '1'
    else:
        print userForm.errors
        return '0'

@main.route('/login', methods=['POST'])
def logIn():
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
        return json.dumps( loginForm.errors, ensure_ascii = False)


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
#   in case there is no meal
    if Ameal.availableNumber <= 0:
        return '0'
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

def SimpleXMLHelper(root, tag):
    node = root.getElementsByTagName(tag)[0]
    node_text = ""
    for node in node.childNodes:
        if node.nodeType in (node.TEXT_NODE, node.CDATA_SECTION_NODE):
            node_text = node_text + node.data
    return node_text

@main.route('/sms', methods=["GET","POST"])
def SMS():
#   generate a 4-bit random number
    number = random.randint(0, 9)
    while number == 0:
        number = random.randint(0, 9)

    number = number * 10 + random.randint(0, 9)
    number = number * 10 + random.randint(0, 9)
    number = number * 10 + random.randint(0, 9)
    print number
    url = SMS_URL + '&mobile=' + str(request.form["phoneNumber"]) + '&content=' + \
    "您的验证码是：" + str(number) + "。请不要把验证码泄露给其他人。"
    print url
    resultXML = urllib2.urlopen(url).read()

    root = minidom.parseString(resultXML)
    code = SimpleXMLHelper( root, "code" )
    print code
    print "code is %r" % code

#   send sms sucessfully
    if code == "2":
        new_sms = SMSModel()
        new_sms.number = number
        new_sms.phoneNumber = request.form["phoneNumber"]
        # one phoneNumber can only have one verification code in the database
        # delete the previous one if exists
        old_code_query = SMSModel.query.filter_by(phoneNumber = request.form["phoneNumber"])
        if old_code_query.count() >= 0:
            old_code = old_code_query.first()
            try:
                db.session.delete( old_code )
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print e

        print "try to add"
        # add the new smsobject into database
        try:
            db.session.add( new_sms )
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print e
            return '0'
        return '1'
    return url

@main.route('/test', methods=['POST', 'GET'])
def test():
    a = Address()
