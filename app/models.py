from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date= db.Column(db.DateTime(timezone=True), default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # comeback and learn sqlalchemy relationships and how to use them. This is a foreign key that references the user table. The user table is created by the User class below. The user table has a one-to-many relationship with the note table. This means that one user can have many notes. The user_id column in the note table is a foreign key that references the id column in the user table. The user_id column is used to link the note to the user who created it.

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(1000))
    notes = db.relationship('Note') # This is a relationship that links the user to the notes they have created. The notes attribute is a list of Note objects that are linked to the user. The backref attribute is used to create a back reference from the Note object to the User object. The backref attribute is used to create a new attribute on the Note object called user. The user attribute is a reference to the User object that created the note. The backref attribute is used to create a new attribute on the User object called notes. The notes attribute is a list of Note objects that are linked to the user.