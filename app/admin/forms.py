from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, FieldList, SelectField, \
        FloatField, IntegerField, BooleanField
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
    amount = IntegerField("amount")
    submit = SubmitField('add')

class PictureForm(Form):
    '''
    picture = FileField('Image file',
            validators = [
                FileRequired(),
                ]
            )
    '''
    type = SelectField(choices=[(0, 'type1'), (1, 'type2')], coerce=int)
    description = StringField('Description:')
    mealList = SelectField(choices=[], coerce=int)
    submit = SubmitField('add')

