from .. import db
from ..models import User, Address
from flask import render_template, request, redirect, url_for
from . import main
from forms import UserForm, LoginForm
import flask

@main.route('/', methods=['POST', 'GET'])
@main.route('/index', methods=['POST', 'GET'])
def index():
    userForm = UserForm()
    loginForm = LoginForm()

    # set the choices of register form(user form)
    addressArray = Address.query.all()
    addresses = []
    for address in addressArray:
        addresses.append( (address.id, address.address) )
    userForm.addresses.choices = addresses

    return render_template('main.html',
            userForm = userForm,
            loginForm = loginForm
            )

@main.route('/register', methods=['POST'])
def register():
    userForm = UserForm(request.form)
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
        return flask.redirect( flask.url_for('.index') )

@main.route('/login', methods=['POST'])
def logIn():
    loginForm = LoginForm(request.form)
    if loginForm.validate_on_submit():
        pass

@main.route('/test', methods=['POST', 'GET'])
def test():
    a = Address()
    return 'ggg'
