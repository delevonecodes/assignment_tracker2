from . import db
from datetime import datetime, date
from flask_login import UserMixin # type: ignore
#from sqlalchemy.sql import func

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    course = db.Column(db.String(150))
    priority = db.Column(db.String(10))
    due_date = db.Column(db.Date)
    notes = db.Column(db.String(1000))
    completion_status = db.Column(db.Boolean, default=False)
    student = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return f'<Assignment {self.id}>'
    
    def days_until_due(self):
        try:
            return (self.due_date - date.today()).days
        except ValueError:
            return 9999

    def due_label(self):
        days = self.days_until_due()
        if self.completion_status:
            return "Completed"
        elif days < -1:
            return f"Overdue by {abs(days)}d"
        elif days == -1:
            return f"Due yesterday"
        elif days == 0:
            return "Due today"
        elif days == 1:
            return "Due tomorrow"
        elif 1 < days <= 6:
            return f"Due in {days} days"
        elif days ==7:
            return "Due in 1 week"
        else:
            return f"Due date: {self.due_date.strftime('%m/%d/%Y')}"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(1000))
    assignments = db.relationship("Assignment")
