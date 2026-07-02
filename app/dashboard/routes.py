from flask import Blueprint, redirect, render_template, flash, request
from flask_login import login_required, current_user
from app.models import Assignment
from app import db

views = Blueprint('views', __name__)

@views.route("/")
def home():
    return render_template("home.html", user=current_user)



@views.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    if request.method == "POST":
        assignment = request.form.get("assignment")
        if len(assignment) < 1:
            flash("Assignment is too short!", category="error")
        else:
            flash("Assignment added!", category="success")
            new_assignment = Assignment(data=assignment, student=current_user.id)
            try:
                db.session.add(new_assignment)
                db.session.commit()
            except Exception as e:
                flash(f"{e} occurred while adding the assignment.", category="error")

    return render_template("dashboard.html", user=current_user)

@views.route("/delete-assignment/<int:id>", methods=["POST"])
def delete_assignment(id):
    assignment = Assignment.query.get_or_404(id)
    try:
        db.session.delete(assignment)
        db.session.commit()
        flash("Assignment deleted!", category="success")
    except Exception as e:
        flash(f"{e} occurred while deleting the assignment.", category="error")
    return redirect("/dashboard")

@views.route("/edit-assignment/<int:id>", methods=["GET", "POST"])
def edit_assignment(id):
    assignment = Assignment.query.get_or_404(id)
    if request.method == "POST":
        assignment.data = request.form.get("assignment")
        try:
            db.session.commit()
            flash("Assignment updated!", category="success")
        except Exception as e:
            flash(f"{e} occurred while updating the assignment.", category="error")
    return render_template("edit.html", assignment=assignment, user=current_user)