from flask import Blueprint, redirect, render_template, flash, request
from flask_login import login_required, current_user
from app.models import Assignment
import datetime
from datetime import date, datetime
from app import db
import calendar

views = Blueprint('views', __name__)

@views.route("/")
def home():
    return render_template("home.html", user=current_user)



@views.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    stats = {
        "completed": sum(1 for assignment in current_user.assignments if assignment.completion_status),
        "incomplete": sum(1 for assignment in current_user.assignments if not assignment.completion_status),
        "rate": (sum(1 for assignment in current_user.assignments if assignment.completion_status) / len(current_user.assignments) * 100) if current_user.assignments else 0,
        "overdue": sum(1 for assignment in current_user.assignments if assignment.days_until_due() < 0)
    }
    today = int(datetime.now().strftime("%d"))

    weeks = [[0, 0, 0, 1, 2, 3, 4], 
             [5, 6, 7, 8, 9, 10, 11], 
             [12, 13, 14, 15, 16, 17, 18], 
             [19, 20, 21, 22, 23, 24, 25], 
             [26, 27, 28, 29, 30, 31, 0]]
    
    try:
        assignments = [(assignment.name, int(assignment.due_date.strftime("%d")), assignment.priority) for assignment in current_user.assignments]
    except Exception:
        assignments = "Error happened"
    
    return render_template("dashboard.html", user=current_user, stats = stats, today = today, current_month_calendar = weeks, assignments = assignments)

@views.route("/assignments", methods = ["GET", "POST"])
@login_required
def assignments():
    if request.method == "POST":
        name = request.form.get("name")
        course = request.form.get("course")
        priority = request.form.get("priority")
        due_date = request.form.get("due_date")
        notes = request.form.get("notes")
        try:
            due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
        except ValueError:
            flash("Invalid due date format. Please use mm/dd/yyyy.", category="error")
            return render_template("dashboard.html", user=current_user)
        try:
            new_assignment = Assignment(name=name, course=course, priority=priority, due_date=due_date, notes=notes, student=current_user.id)
            db.session.add(new_assignment)
            db.session.commit()
            flash("Assignment added!", category="success")
        except Exception as e:
            flash(f"Error occurred while adding the assignment, please try again.", category="error")
            print(f"Error occurred while adding the assignment: {e}")
    return render_template("assignments.html", user=current_user)


@views.route("/delete-assignment/<int:id>", methods=["POST"])
@login_required
def delete_assignment(id):
    assignment = Assignment.query.get_or_404(id)
    try:
        db.session.delete(assignment)
        db.session.commit()
        flash("Assignment deleted!", category="success")
    except Exception as e:
        flash(f"Error occurred while deleting the assignment, please try again.", category="error")
        print(f"Error occurred while deleting the assignment: {e}")
    return redirect("/assignments")

@views.route("/edit-assignment/<int:id>", methods=["GET", "POST"])
@login_required
def edit_assignment(id):
    assignment = Assignment.query.get_or_404(id)
    if request.method == "POST":
        due_date = request.form.get("due_date")
        try:
            due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
        except ValueError:
            flash("Invalid due date format. Please use mm/dd/yyyy.", category="error")
            return render_template("edit.html", assignment=assignment, user=current_user)
        assignment.name = request.form.get("name")
        assignment.course = request.form.get("course")
        assignment.priority = request.form.get("priority")
        assignment.notes = request.form.get("notes")
        assignment.completion_status = request.form.get("completed") == "True"
        assignment.due_date = due_date
        try:
            db.session.commit()
            flash("Assignment updated!", category="success")
        except Exception as e:
            flash(f"Error occurred while updating the assignment, please try again.", category="error")
            print(f"Error occurred while updating the assignment: {e}")
    return render_template("edit.html", assignment=assignment, user=current_user)