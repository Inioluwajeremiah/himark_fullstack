from datetime import datetime
from flask_login import UserMixin
from . import db
from sqlalchemy.sql import func


class HotelModel(db.Model):
    # __bind_key__ = 'hotel_records'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    middlename = db.Column(db.String(50))
    roomtype = db.Column(db.String(50))
    roomno = db.Column(db.String(50))
    duration = db.Column(db.String(50))
    purpose = db.Column(db.String(50))

    dateTime = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)


class AdminModel(UserMixin, db.Model):
    # __bind_key__ = 'admin_db'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)
    hashedPassword = db.Column(db.String(150), index=True)

    # def set_password(self, password):pyt
    #     self.password_hash = generate_password_hash(password)

    # def check_password(self, password):
    #     return check_password_hash(self.password_hash, password)
