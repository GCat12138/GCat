# encoding:utf8
from flask.ext.wtf import Form
from wtforms import StringField,SubmitField, FieldList, SelectField,\
        PasswordField
from wtforms.validators import Required, Length
import wtforms
from ..models import Address

class UserForm(Form):
    phoneNumber = StringField(validators=[Required()])
    nickName = StringField()
    password = PasswordField(validators=[Required(), Length(min=6, max=15)])
    verification = StringField("验证码", validators=[Required()])
    addresses = SelectField(choices=[], coerce=int)
    #submit = SubmitField("Register")

class LoginForm(Form):
    phoneNumber = StringField(validators=[Required(), Length(min=11, max=11)])
    password = PasswordField(validators=[Required()])
    #submit = SubmitField("Log In")

class SMSForm(Form):
    phoneNumber = StringField(validators=[Required(), Length(min=11, max=11)])
    pass
