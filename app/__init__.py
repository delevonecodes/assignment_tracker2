from flask import Flask, app
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dawydgawiydgaiwd qwawdaiwadawd'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    

    from app.auth.routes import auth
    from app.dashboard.routes import views

    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(views, url_prefix="/")


    from .models import User, Note

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    if not path.exists('app/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')

    return app
    