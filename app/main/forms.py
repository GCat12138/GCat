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
    addresses = SelectField(u"地址",choices=[], coerce=int)
    submit = SubmitField(u"提交")

class LoginForm(Form):
    phoneNumber = StringField(validators=[Required(), Length(min=11, max=11)])
    password = PasswordField(validators=[Required()])
    #submit = SubmitField("Log In")

class SMSForm(Form):
    phoneNumber = StringField(validators=[Required(), Length(min=11, max=11)])
    pass
