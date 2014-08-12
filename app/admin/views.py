#encoding:utf8
from . import admin
from werkzeug import secure_filename
from flask import render_template, request
from forms import AddressForm, MealForm, PictureForm, AMealForm
from ..models import Address, Meal, Picture, ActualMeal, Order
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
        discount = form.discount.data
        amount = form.price.data

        newMeal = Meal()
        newMeal.description = description
        newMeal.price = price
        newMeal.discount = discount
        #newMeal.amount = amount

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

@admin.route('/deletePic', methods=['POST'])
def deletePic():
    picID = request.form["id"]
    if picID is not None:
        pic = Picture.query.get( picID )
        if pic is not None:
            picName = pic.name
            picURL = os.path.join( PICTURE_DIR, picName)
            print picURL
            try:
                os.remove( picURL )
            except Exception:
                pass
            try:
                db.session.delete( pic )
                db.session.commit()
            except Exception:
                db.session.rollback()
                return '0'
        print request.form["id"]
    return "1"

@admin.route('/pic', methods=['GET', 'POST'])
def editPic():
    form = PictureForm(request.form)
    form.mealList.choices = [(m.id, m.description) for m in Meal.query.all()]

    if form.validate_on_submit():
        type = form.type.data
        description = form.description.data
        p_title = form.title.data
        mealID = form.mealList.data
        pictFile = request.files['pic']
        if pictFile:
            filename = secure_filename(pictFile.filename)

            print filename

            #Current time
            dateT = datetime.datetime.now()
            dateString = dateT.strftime("%Y_%m_%d_%H_%M_%S")
            pictureArray = Picture.query.all()
            pictCnt = len(pictureArray)

            pictURL = os.path.join(PICTURE_DIR,
                    dateString + "_" + str(pictCnt) + "_" + filename)

            newPic = Picture()
            newPic.description = description
            newPic.title = p_title
            newPic.mealId = mealID
            newPic.type = type
            newPic.name = dateString + "_" + str(pictCnt) + "_" + filename
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

    pics = Picture.query.all()
    return render_template(
            'admin/picture.html',
            form = form,
            pics = pics
            )

@admin.route('/deleteAmeal', methods=['POST'])
def deleteAMeal():
    form = AMealForm(request.form)
    form.mealList.choices = [
            (meal.id, meal.description) for meal in Meal.query.all()]
    form.addressList.choices =[
            (address.id, address.address) for address in Address.query.all()]

    if form.validate_on_submit():
        current_ameal = ActualMeal.query.get( int(form.id.data) )
        try:
            db.session.delete( current_ameal )
            db.session.commit()
        except Exception as e:
            print e
            db.session.rollback()
            return '0'
        return '1'
    else:
        return '0'

@admin.route('/editAmeal', methods=['POST'])
def editAMeal():
    form = AMealForm(request.form)
    form.mealList.choices = [
            (meal.id, meal.description) for meal in Meal.query.all()]
    form.addressList.choices =[
            (address.id, address.address) for address in Address.query.all()]

    if form.validate_on_submit():
        current_ameal = ActualMeal.query.get( int(form.id.data) )
        current_ameal.addressId = form.addressList.data
        current_ameal.amount = form.amount.data
        current_ameal.availableNumber = form.availableNumber.data
        current_ameal.mealID = form.mealList.data
        current_ameal.date = form.date.data

        startTime = form.startTime.data
        current_ameal.startTime = \
                datetime.time( startTime.hour, startTime.minute )

        endTime = form.endTime.data
        current_ameal.endTime = \
                datetime.time( endTime.hour, endTime.minute )

        try:
            db.session.add( current_ameal )
            db.session.commit()
        except:
            db.session.rollback()
            return '0'

        return '1'

    else:
        print form.errors
        return '0'

@admin.route('/ameal', methods=['POST', 'GET'])
def AMeal():
    form = AMealForm(request.form)

    form.mealList.choices = [
            (meal.id, meal.description) for meal in Meal.query.all()]
    form.addressList.choices =[
            (address.id, address.address) for address in Address.query.all()]
    if form.validate_on_submit():
        mealID = form.mealList.data
        addressID = form.addressList.data
        amount = form.amount.data

        actualMeal = ActualMeal()
        actualMeal.addressId = addressID
        actualMeal.amount = amount
        actualMeal.mealID = mealID
        actualMeal.availableNumber = amount
        actualMeal.date = form.date.data

        formTime = form.startTime.data
        actualMeal.startTime = datetime.time(formTime.hour, formTime.minute)

        formTime = form.endTime.data
        actualMeal.endTime = datetime.time( formTime.hour, formTime.minute )

        try:
            db.session.add( actualMeal )
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print e
            return '0'

        return "succeed"

    ameals = ActualMeal.query.all()
    formList = []
    for ameal in ameals:
        tempForm = AMealForm()
        tempForm.mealList.choices = [
                (meal.id, meal.description) for meal in Meal.query.all()]
        tempForm.addressList.choices =[
                (address.id, address.address) for address in Address.query.all()]
        tempForm.addressList.data = ameal.addressId
        tempForm.amount.data = ameal.amount
        tempForm.availableNumber.data = ameal.availableNumber
        tempForm.mealList.data = ameal.mealID
        tempForm.date.data = ameal.date
        tempForm.startTime.data = ameal.startTime
        tempForm.endTime.data = ameal.endTime
        tempForm.id.data = ameal.id

        formList.append( tempForm )

    return render_template('admin/ameal.html',
            form=form,
            ameals = ameals,
            tForms = formList
            )

@admin.route('/order', methods=['POST', 'GET'])
def EditOrder():
    orders = Order.query.order_by(Order.time.desc())
    return render_template('admin/order.html', orders = orders)
