from flask import Blueprint, redirect, render_template, flash, request
from flask_login import login_required, current_user
from app.models import Assignment
import datetime
from datetime import date, datetime
from app import db
from app.cal import get_month_info

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
        "rate": round((sum(1 for assignment in current_user.assignments if assignment.completion_status) / len(current_user.assignments) * 100), 2) if current_user.assignments else 0,
        "overdue": sum(1 for assignment in current_user.assignments if assignment.days_until_due() < 0 and not assignment.completion_status)
    }
    today = int(datetime.now().strftime("%d"))
    upcoming_assignments = sorted([assignment for assignment in current_user.assignments if 0 <= assignment.days_until_due() <= 7], key = lambda a: a.days_until_due())

    month_info = get_month_info()
    
    try:
        assignments = [(assignment.name, int(assignment.due_date.strftime("%d")), assignment.priority) for assignment in current_user.assignments if not assignment.completion_status ]
    except Exception:
        assignments = "Error happened"
    
    return render_template("dashboard.html", user=current_user, stats = stats, today = today, current_month_calendar = month_info, assignments = assignments, upcoming_assignments = upcoming_assignments)

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
        except Exception:
            flash("Invalid due date format. Please use mm/dd/yyyy.", category="error")
            return render_template("dashboard.html", user=current_user)
        try:
            new_assignment = Assignment(name=name, course=course, priority=priority, due_date=due_date, notes=notes, student=current_user.id)
            db.session.add(new_assignment)
            db.session.commit()
            flash("Assignment added!", category="success")
        except ValueError as e:
            flash(f"Error occurred while adding the assignment, please try again.", category="error")
            print(f"Error occurred while adding the assignment: {e}")

    search_query = request.args.get("search", "").strip()
    sort_by = request.args.get("sorting-method", "Default")

    query = Assignment.query.filter_by(student=current_user.id)

    if search_query:
        query = query.filter(Assignment.name.ilike(f"%{search_query}%"))

    if sort_by == "Due Date":
        query = query.order_by(Assignment.due_date)
    elif sort_by == "Name":
        query = query.order_by(Assignment.name)
    elif sort_by == "Course":
        query = query.order_by(Assignment.course)
    elif sort_by == "Priority":
        from sqlalchemy import case
        priority_order = case(
            (Assignment.priority == "High", 1),
            (Assignment.priority == "Medium", 2),
            (Assignment.priority == "Low", 3),
            else_=4
        )
        query = query.order_by(priority_order)
    elif sort_by == "Completed":
        query = query.filter(Assignment.completion_status.is_(True))
    elif sort_by == "Incomplete":
        query = query.filter(Assignment.completion_status.is_(False))

    assignments = query.all()
    print(assignments)


    return render_template("assignments.html", user=current_user, assignments = assignments)


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