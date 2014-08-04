#encoding: utf8
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, FieldList, SelectField, \
        FloatField, IntegerField, BooleanField, DateTimeField, \
        DateField
from wtforms.validators import Required
from flask_wtf.file import FileRequired, FileAllowed, FileField
import wtforms

class AddressForm(Form):
    address = StringField("Address:", validators=[Required()])
    submit = SubmitField('add')

class MealForm(Form):
    description = StringField("Description:")
    price = FloatField("Price")
    discount = FloatField("Discount")
#    amount = IntegerField("amount")
    submit = SubmitField('add')

class PictureForm(Form):
    '''
    picture = FileField('Image file',
            validators = [
                FileRequired(),
                ]
            )
    '''
    type = SelectField(choices=[(0, 'main'), (1, 'meal'), (2, 'material')], coerce=int)
    description = StringField('Description:')
    mealList = SelectField(choices=[], coerce=int)
    submit = SubmitField('add')

class AMealForm(Form):
    id = IntegerField("id")
    mealList = SelectField(choices=[], coerce=int)
    addressList = SelectField(choices=[], coerce=int)
    amount = IntegerField(u"总数量")
    availableNumber = IntegerField(u"剩余数量")
    date = DateField(u"日期")
    startTime = DateTimeField(format='%H:%M')
    endTime = DateTimeField(format='%H:%M')
    submit = SubmitField(u"提交")

