import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import path
from flask_login import LoginManager

# load_dotenv() with no path only finds app/.env if the process cwd happens
# to be app/ — pointing at the file directly makes it work regardless of
# where main.py is run from.
load_dotenv(Path(__file__).resolve().parent / ".env")
db = SQLAlchemy()

DATABASE_URL = os.environ.get("DATABASE_URL")

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL or 'sqlite:///database.db'
    db.init_app(app)
    Migrate(app, db)


    from app.auth.routes import auth
    from app.dashboard.routes import views
    from app.api.routes import api

    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(api, url_prefix="/api")

    from .models import User, Assignment, LinkCode

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