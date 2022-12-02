from flask import Blueprint
from flask.json import jsonify
from flask import render_template, request, url_for, redirect
from flask_login import login_required, current_user
from sqlalchemy.sql.functions import user
from full_stack.models import HotelModel
import json
from . import db
from .models import HotelModel, AdminModel

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def dataPage():
    allRecords = HotelModel.query.all()
    if not allRecords:
        return render_template('main.html', user=current_user)
    else:
        return render_template('main.html',
                               allRecords=allRecords,
                               user=current_user)


@views.route('/register', methods=['GET', 'POST'])
@login_required
def addNewGuests():
    if request.method == "POST":

        if request.form.get('register') == "Register":
            firstname = request.form.get('firstname')
            lastname = request.form.get('lastname')
            middlename = request.form.get('middlename')
            roomtype = request.form.get('roomtype')
            roomno = request.form.get('roomno')
            duration = request.form.get('duration')
            purpose = request.form.get('purpose')

            print(firstname, lastname, middlename, roomtype, roomno, duration,
                  purpose)
            # if not firstname or not lastname or not middlename or not roomtype or not roomno or not duration or not purpose:
            #     fill_fields = "Ensure you fill all fields"
            #     return render_template('register.html',
            #                            user=current_user,
            #                            fill_fields=fill_fields)
            if firstname and lastname and middlename and roomtype and roomno and duration and purpose:
                hostelRecords = HotelModel(firstname=firstname,
                                           lastname=lastname,
                                           middlename=middlename,
                                           roomtype=roomtype,
                                           roomno=roomno,
                                           duration=duration,
                                           purpose=purpose)
                db.session.add(hostelRecords)
                db.session.commit()

                smsg = firstname + ' ' + lastname + ' successfully registered'
                return render_template('register.html',
                                       smsg=smsg,
                                       user=current_user)
            else:
                fill_fields = "fill all fields"
                # Ensure you
                return render_template('register.html',
                                       user=current_user,
                                       fill_fields=fill_fields)

        else:
            # db.drop_all()
            # db.create_all()
            return render_template('register.html', user=current_user)

    return render_template('register.html', user=current_user)


#   D E L E T E         B U T T O N
@views.route("/delrow", methods=['POST'])
def deleteRow():
    students_records = json.loads(request.data)
    row_id = students_records['row_id']
    deleteUser = HotelModel.query.get(row_id)
    if deleteUser:
        db.session.delete(deleteUser)
        db.session.commit()
    return jsonify({})
    # return redirect(request.url)
    # return render_template('main.html')


#  A D M I N     R E C O R D S
@views.route("/ad_records")
@login_required
def adminRecords():
    # return redirect(request.url)
    adminRecords = AdminModel.query.all()
    if not adminRecords:
        # return render_template('main.html', allRecords = allRecords)
        return render_template('adminRecord.html', user=current_user)
    else:
        return render_template('adminRecord.html',
                               adminRecords=adminRecords,
                               user=current_user)


#  S E A R C H
@views.route('/search', methods=['POST'])
def search():
    if request.method == "POST":
        if request.form.get('search') == 'Search':
            allRecords = HotelModel.query.all()
            searchvalue = request.form.get('search-text')
            if not searchvalue:
                fill_fields = "Search field cannot be empty"
                return render_template('main.html',
                                       allRecords=allRecords,
                                       fill_fields=fill_fields,
                                       user=current_user)
            else:
                # searchvalue = searchvalue.lower()
                searchUsers = HotelModel.query.filter_by(lastname=searchvalue)
                return render_template('search.html',
                                       searchUsers=searchUsers,
                                       user=current_user)
        return render_template('main.html', user=current_user)


@views.route("/forbidden", methods=['GET', 'POST'])
@login_required
def protected():
    return redirect(url_for('forbidden.html'))


#   E D I T


@views.route("/edit/<id>")
def editRecord(id):
    editRecord = HotelModel.query.filter_by(id=id).first()
    # return redirect(request.url)
    return render_template('update.html',
                           edit_record=editRecord,
                           user=current_user)


#  U P D A T E
@views.route("/update/<id>", methods=['POST'])
def updateRecord(id):

    if request.method == "POST":
        allRecords = HotelModel.query.all()
        if request.form.get('update') == "Update":
            firstname = request.form.get('ufirstname')
            lastname = request.form.get('ulastname')
            middlename = request.form.get('umiddlename')
            roomtype = request.form.get('uroomtype')
            roomno = request.form.get('roomno')
            duration = request.form.get('uduration')
            purpose = request.form.get('purpose')

            hostelRecords = HotelModel(firstname=firstname,
                                       lastname=lastname,
                                       middlename=middlename,
                                       roomtype=roomtype,
                                       roomno=roomno,
                                       duration=duration,
                                       purpose=purpose)

            edit_record = HotelModel.query.filter_by(id=id).first()
            edit_record.firstname = firstname
            edit_record.lastname = lastname
            edit_record.middlename = middlename
            edit_record.roomtype = roomtype
            edit_record.roomno = roomno
            edit_record.duration = duration
            edit_record.purpose = purpose

            # db.session.add(hostelRecords )
            db.session.commit()
            return render_template('main.html',
                                   post=allRecords,
                                   user=current_user)
            # return redirect(url_for('dataPage'))

    return render_template('update.html', user=current_user)


# D E L E T E    ADMIN
@views.route("/delete/<id>")
def delete(id):
    deleteUser = AdminModel.query.filter_by(id=id).first()
    db.session.delete(deleteUser)
    db.session.commit()
    # return redirect(request.url)
    return redirect(url_for('views.adminRecords'))
