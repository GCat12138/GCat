from flask.ext.wtf import Form
from wtforms import StringField,SubmitField, FieldList, SelectField,\
        PasswordField
from wtforms.validators import Required
import wtforms
from ..models import Address

class UserForm(Form):
    phoneNumber = StringField(validators=[Required()])
    nickName = StringField()
    password = PasswordField(validators=[Required()])

    addresses = SelectField(choices=[], coerce=int)
    submit = SubmitField("Register")

class LoginForm(Form):
    phoneNumber = StringField(validators=[Required()])
    password = PasswordField(validators=[Required()])
    submit = SubmitField("Log In")
