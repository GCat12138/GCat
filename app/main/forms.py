# encoding:utf8
from flask.ext.wtf import Form
from wtforms import StringField,SubmitField, FieldList, SelectField,\
        PasswordField
from wtforms.validators import Required, Length
import wtforms
from ..models import Address

class UserForm(Form):
    phoneNumber = StringField(u"手机号",validators=[Required()])
    password = PasswordField(u"密码",validators=[Required(), Length(min=6, max=15)])
    verification = StringField(u"验证码", validators=[Required()])
    nickName = StringField(u"昵称")
    addresses = SelectField(u"",choices=[], coerce=int)
    submit = SubmitField(u"提交")

class LoginForm(Form):
    phoneNumber = StringField(u"手机号",validators=[Required(), Length(min=11, max=11)])
    password = PasswordField(u"密码", validators=[Required()])
    submit = SubmitField(u"提交")

class SMSForm(Form):
    phoneNumber = StringField(validators=[Required(), Length(min=11, max=11)])

class OrderForm(Form):
    actualMealID = FieldList()
    submit = SubmitField(u"闪电抢食")

class ChangePasswordForm(Form):
    phoneNumber = StringField(u"手机号",validators=[Required()])
    oldPassword = PasswordField(u"旧密码",validators=[Required(), Length(min=6, max=15)])
    newPassword = PasswordField(u"新密码",validators=[Required(), Length(min=6, max=15)])
    submit = SubmitField(u"提交")

class ForgotPasswordForm(Form):
    phoneNumber = StringField(u"手机号", validators=[Required(), Length(min=11, max=11)])
    verification = StringField(u"验证码", validators=[Required()])
    password = PasswordField(u"新密码", validators=[Required(), Length(min=6, max=15)])
    submit = SubmitField(u"提交")

