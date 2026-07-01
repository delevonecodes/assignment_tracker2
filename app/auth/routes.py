from flask import Blueprint, flash, render_template, request, redirect, url_for
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")

        if not name or not password:
            flash("Please fill out all fields.", category="error")
            return render_template("login.html")

        user_by_username = User.query.filter_by(username=name).first()
        user_by_email = User.query.filter_by(email=name).first()
        if user_by_username:
            if check_password_hash(user_by_username.password, password):
                flash("Logged in successfully!", category="success")
                login_user(user_by_username, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password, try again.", category="error")
        elif user_by_email:
            if check_password_hash(user_by_email.password, password):
                flash("Logged in successfully!", category="success")
                login_user(user_by_email, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password, try again.", category="error")
        else:
            flash("Email or username does not exist.", category="error")
    return render_template("login.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        password2 = request.form.get("password2")

        user_by_email = User.query.filter_by(email=email).first()
        user_by_username = User.query.filter_by(username=username).first()

        def validate_password(p):
            pass

        if user_by_email:
            flash("Email already exists.", category="error")
        elif user_by_username:
            flash("Username already exists.", category="error")
        elif len(email) < 4:
            flash("Email must be greater than 4 characters.", category="error")
        elif len(username) < 3:
            flash("Username must be greater than 3 characters.", category="error")
        elif password != password2:
            flash("Passwords must match.", category="error")
        elif len(password) < 7:
            flash("Password must be at least 7 characters.", category="error")
        else:
            user = User(email=email, username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            flash("Account created!", category="success")
            login_user(user, remember=True)
            return redirect(url_for("views.home"))

    return render_template("sign_up.html", user=current_user)
