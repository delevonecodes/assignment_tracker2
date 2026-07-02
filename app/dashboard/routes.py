from flask import Blueprint, render_template, flash, request
from flask_login import login_required, current_user
from app.models import Note
from app import db

views = Blueprint('views', __name__)

@views.route("/")
def home():
    return render_template("home.html", user=current_user)



@views.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    if request.method == "POST":
        note = request.form.get("note")
        if len(note) < 1:
            flash("Note is too short!", category="error")
        else:
            flash("Note added!", category="success")
            new_note = Note(data=note, user_id=current_user.id)
            try:
                db.session.add(new_note)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                flash(f"{e} occurred while adding the note.", category="error")

    return render_template("dashboard.html", user=current_user)

@views.route("/delete-note/<int:id>", methods=["POST"])
def delete_note(id):
    task = Note.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
        flash("Note deleted!", category="success")
    except Exception as e:
        db.session.rollback()
        flash(f"{e} occurred while deleting the note.", category="error")
    return render_template("dashboard.html", user=current_user)

@views.route("/edit-note/<int:id>", methods=["GET", "POST"])
def edit_note(id):
    note = Note.query.get_or_404(id)
    if request.method == "POST":
        note.data = request.form.get("note")
        try:
            db.session.commit()
            flash("Note updated!", category="success")
        except Exception as e:
            db.session.rollback()
            flash(f"{e} occurred while updating the note.", category="error")
    return render_template("edit.html", note=note, user=current_user)