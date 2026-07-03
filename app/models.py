from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    course = db.Column(db.String(150))
    priority = db.Column(db.String(150))
    due_date = db.Column(db.String())
    notes = db.Column(db.String(10000))
    student = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return f'<Assignment {self.id}>'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(1000))
    assignments = db.relationship("Assignment")