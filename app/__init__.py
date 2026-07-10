import os
from dotenv import load_dotenv
from flask import Flask, app
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

load_dotenv()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    db.init_app(app)

    from app.auth.routes import auth
    from app.dashboard.routes import views

    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(views, url_prefix="/")


    from .models import User, Assignment

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    if not path.exists('app/' + "database.db"):
        with app.app_context():
            db.create_all()
        print('Created Database!')

    return app
    
