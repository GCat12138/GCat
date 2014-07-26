from . import admin
from werkzeug import secure_filename
from flask import render_template, request
from forms import AddressForm, MealForm, PictureForm
from ..models import Address, Meal, Picture
from .. import db
import os
import datetime
from app.shareVars import BASE_DIR

PICTURE_DIR = os.path.join(BASE_DIR, 'static/pic')

@admin.route('/')
def index():

    print PICTURE_DIR
    return render_template('admin/index.html')

@admin.route('/address', methods=['GET','POST'])
def editAddress():
    form = AddressForm(request.form)
    if form.validate_on_submit():
        address = form.address.data
        print address
        newAddress = Address(address)
        print newAddress.address
        db.session.add(newAddress)
        db.session.commit()
        return 'success'

    addresses = Address.query.all()
    return render_template(
            'admin/address.html',
            form=form,
            addresses=addresses
            )

@admin.route('/meal', methods=['GET', 'POST'])
def editMeal():
    form = MealForm(request.form)

    if form.validate_on_submit():
        description = form.description.data
        price = form.price.data
        discount = form.price.data
        amount = form.price.data

        newMeal = Meal()
        newMeal.description = description
        newMeal.price = price
        newMeal.discount = discount
        newMeal.amount = amount

        try:
            db.session.add( newMeal )
            db.session.commit()
        except Exception as e:
            print e
            db.session.rollback()
            return 'failed'
        return 'success'

    return render_template(
           'admin/meal.html',
           form = form
           )

@admin.route('/pic', methods=['GET', 'POST'])
def editPic():
    form = PictureForm(request.form)
    form.mealList.choices = [(m.id, m.description) for m in Meal.query.all()]

    if form.validate_on_submit():
        type = form.type.data
        description = form.description.data
        mealID = form.mealList.data
        pictFile = request.files['pic']
        if pictFile:
            filename = secure_filename(pictFile.filename)

            #Current time
            dateT = datetime.datetime.now()
            dateString = dateT.strftime("%Y_%m_%d_%H_%M_%S")
            pictureArray = Picture.query.all()
            pictCnt = len(pictureArray)

            pictURL = os.path.join(PICTURE_DIR,
                    dateString + "_" + str(pictCnt) + "_" + filename)

            newPic = Picture()
            newPic.description = description
            newPic.mealId = mealID
            newPic.type = type
            newPic.url = pictURL
            try:
                db.session.add( newPic )
                db.session.commit()
                pictFile.save( pictURL )
            except Exception as e:
                print e
                db.session.rollback()
                return 'failed'
        return 'uploaded'
    else:
        #print form.picture.data
        print form.errors

    return render_template(
            'admin/picture.html',
            form = form
            )
