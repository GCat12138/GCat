# coding=utf8
from .. import db
from ..models import User, Address, ActualMeal, Meal, Picture, Order,\
        SMSModel, LikeModel
from flask import render_template, request, redirect, url_for, flash, jsonify
from . import main
from forms import UserForm, LoginForm, SMSForm, ChangePasswordForm,\
        ForgotPasswordForm
from flask.ext.login import current_user, login_user, logout_user,\
        login_required
import flask
import datetime, time
from sqlalchemy import and_, or_
import json
import urllib2, urllib
from ..shareVars import SMS_URL, SMS_ACCOUNT, SMS_PASSWORD
from xml.dom import minidom
import random
from .. import redis
from manage import app

@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main.before_app_request
def before_request():
    # for counting online users
    if current_user.is_authenticated():
        #make_online( current_user.id )
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
@main.route('/<addressName>', methods=['GET'])
@main.route('/index/', methods=['GET'])
@main.route('/index/<addressName>', methods=['GET'])
def index(addressName = None):
    today_date = datetime.date.today()
    current_datetime = datetime.datetime.now()
    current_time = datetime.time(
               current_datetime.hour,
               current_datetime.minute,
               current_datetime.second,
               current_datetime.microsecond
            )

    addressID = None
    if addressName is not None:
        current_address = Address.query.filter_by( address = addressName ).first()
        if current_address:
            addressID = current_address.id

    if addressID is None:
        if current_user.is_authenticated():
            addressID = current_user.addressId
        else:
            current_address = Address.query.first()

            if current_address:
                addressID = current_address.id

    if addressID is not None:
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

    if addressID is None:
        return render_template('index.html',
                userForm = userForm,
                loginForm = loginForm,
                )


    # store the information of this meal, not the actual meal
    mealInformation = None
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

#    print get_online_users()

    if mealInformation:
        people = random.randint(300, 400)
        return render_template('index.html',
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
                sForm = SMSForm(),
                population = people
                )
    else:
        return render_template('index.html',
                userForm = userForm,
                loginForm = loginForm,
                )

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
            print "sms-code"
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
    registerForm = UserForm(request.form)
    registerForm.addresses.choices = [
            (address.id, address.address) for address in Address.query.all()
        ]
    if registerForm.validate_on_submit():
        phoneNumber = registerForm.phoneNumber.data
        if User.query.filter_by(phoneNumber = phoneNumber).count() != 0:
            #user already exists, jump to log in
            return jsonify( success = 2, msg="手机号已注册, 请直接登录")
        print "try to register"
        result = register_helper_function()
        print result
        if result == "1":
            #register successfully
            return jsonify( success = 1)
        else:
            return jsonify( success = 0, msg="注册失败")
    else:
        print registerForm.errors

    return jsonify( success = 0 )


def loginHelper(phoneNumber, password):
    user = User.query.filter_by( phoneNumber = phoneNumber).first()
    if user is not None and user.verify_password( password ):
        login_user(user, remember=True)
        print "log in success"
        return '1'
    else:
        print 'no such user'
        return '0'


@main.route('/login', methods=['POST'])
def logIn():
    loginForm = LoginForm(request.form)
    if loginForm.validate_on_submit():
        result = loginHelper(
                loginForm.phoneNumber.data,
                loginForm.password.data
                )
        if result == "1":
            return jsonify(success = 1)
        else:
            return jsonify(
                    success=0,
                    msg="用户账号密码错误或者该用户不存在"
            )

    else:
        print loginForm.errors

    return jsonify(
                success=0
            )


@main.route('/logout')
@login_required
def LogOut():
    logout_user()
    return redirect( url_for('main.index') )

@main.route('/like', methods=['POST'])
def Like():
    mealId = request.form['mealId']
    newLike = LikeModel()
    newLike.mealID = mealId
    newLike.userID = current_user.id
    try:
        db.session.add(newLike)
        db.session.commit()
    except Exception as e:
        print e
        return '0'

    return '1'
    pass

def MakeOrderHelperFunction( amealID ):
    newOrder = Order()
    Ameal = ActualMeal.query.get( int(amealID) )
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
    newOrder.amealId = Ameal.id
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
    return newOrder

def postHelper(url, data):
    req = urllib2.Request( url )
    data = urllib.urlencode( data )
    #enable cookie
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    response = opener.open( req, data )
    return response.read()

@main.route('/make_order/<int:amealID>', methods=['GET'])
def MakeOrder( amealID ):
    if current_user.is_authenticated():
        if Order.query.filter_by(amealId=amealID, userID = current_user.id).count() == 0:
            result = MakeOrderHelperFunction( amealID )
            Ameal = ActualMeal.query.get( amealID )
            meal = Meal.query.get( Ameal.mealID)
            address = Address.query.get( Ameal.addressId)
            if result != '0':
                url = "http://106.ihuyi.cn/webservice/sms.php?method=Submit"

                content = "终于抢到啦！美食家%s，您抢到了第%s份美食！原价%s，现在竟然只要%s元！美食在%s门口躺着等你来！带好手机～带好票子～带好食欲～我们12：00不见不散！PS：吃完记得点赞噢～" % (current_user.nickName, str(result.number), str(meal.price), str( meal.price * meal.discount),address.address)
                data = {
                        "account" : SMS_ACCOUNT,
                        "password" : SMS_PASSWORD,
                        "mobile" : str(current_user.phoneNumber),
                        "content" : content
                }
                print content
                resultXML = postHelper( url, data )
                print resultXML
                root = minidom.parseString(resultXML)
                code = SimpleXMLHelper( root, "code" )
                print code
                print "order code is %r" % code
                msg = SimpleXMLHelper( root, "msg" )
                print msg

                getMessage = {
                    "nickName": current_user.nickName,
                    "resultNum": str(result.number),
                    "mealPrice": str( meal.price * meal.discount),
                    "oldPrice": str(meal.price),
                    "getAddress": address.address
                }
                return render_template("success.html",
                        msg= getMessage
                        )
            else:
                return 'No'  #there are no food
        else:
            return render_template("success.html",
                        msg= "sorry" #get food twice or more
                    )

@main.route("/reg_login")
def RegLogin():
    userForm = UserForm(request.form)
    userForm.addresses.choices = [
        (address.id, address.address) for address in Address.query.all()
    ]
    loginForm = LoginForm(request.form)

    return render_template("make_order.html",
                userForm = userForm,
                loginForm = loginForm
            )


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
    url = SMS_URL + '&mobile=' + str(request.form["phoneNumber"]) +\
            '&content=' "亲爱的美食家：您的手机验证码为" + str(number) +\
            "。迅速注册下单，诱人美食等你来！"
    print url
    resultXML = urllib2.urlopen(url).read()

    root = minidom.parseString(resultXML)
    code = SimpleXMLHelper( root, "code" )
    msg = SimpleXMLHelper( root , "msg")
    print msg
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

#Crap, they don't want this
@main.route('/change_password', methods=["GET", "POST"])
def ChangePassword():
    cPasswordForm = ChangePasswordForm(request.form)
    if cPasswordForm.validate_on_submit():
        old_user = User.query.filter_by(
                phoneNumber = cPasswordForm.phoneNumber.data).first()
        if old_user:
            if old_user.verify_password(cPasswordForm.oldPassword.data):
                old_user.password = cPasswordForm.newPassword.data
                try:
                    db.session.add( old_user )
                    db.session.commit()
                except Exception as e:
                    db.rollback()
                    print e
                    return render_template("success.html",
                                msg = u"恭喜你，修改成功"
                            )

            else:
                return render_template("success.html",
                            msg = u"密码错误"
                        )

    return render_template("change_password.html",
            cp_form = cPasswordForm
            )

@main.route('/check_phoneNumber/<int:phoneNumber>')
def checkPhoneNumber(phoneNumber):
    if User.query.filter_by(phoneNumber = phoneNumber).count() == 0:
        #No such user
        return '0'
    else:
        #user exists
        return '1'

@main.route('/forgot_password', methods=["GET", "POST"])
def ForgotPassword():
    forgotForm = ForgotPasswordForm( request.form )
    if forgotForm.validate_on_submit():
        verification_code = forgotForm.verification.data
        phoneNumber = forgotForm.phoneNumber.data
        password = forgotForm.password.data

        print phoneNumber
        print password

        sms_code = SMSModel.query.filter_by(phoneNumber = phoneNumber).first()
        if sms_code.number != int(verification_code):
            flash(u"验证码输入错误，请重新获取")
        else:
            user = User.query.filter_by(phoneNumber = phoneNumber).first()
            if user is None:
                flash(u"该手机号还未注册")
            else:
                user.password = password
                try:
                    db.session.add( user )
                    db.session.commit()
                except Exception as e :
                    print e
                    db.session.rollback()
                    flash(u"更改失败")
                    return render_template(
                                "forgot.html",
                                forgot_form = forgotForm
                                )


                return redirect( url_for("main.LogOut") )

    return render_template(
                "forgot.html",
                forgot_form = forgotForm
                )
    pass

@main.route('/test', methods=['POST', 'GET'])
def test():
    a = Address()

# show online users helpers
def make_online(user_id):
    now = int(time.time())
    expires = now + (app.config["ONLINE_LAST_MINUTES"] * 60) + 10
    all_users_key = 'online-users/%d' % (now // 60)
    user_key = 'user-activity/%s' % user_id
    p = redis.pipeline()
    p.sadd(all_users_key, user_id)
    p.set( user_key, now )
    p.expireat( all_users_key, expires)
    p.expireat( user_key, expires )
    p.execute()

def get_user_last_activity(user_id):
    last_active = redis.get( 'user-activity/%s' % user_id )
    if last_active is None:
        return None
    return datetime.datetime.utcfromtimestamp( int(last_active) )

def get_online_users():
    current = int(time.time())
    minutes = xrange(app.config['ONLINE_LAST_MINUTES'])
    return redis.sunion( ['online-users/%d' % (current - x) for x in minutes])

