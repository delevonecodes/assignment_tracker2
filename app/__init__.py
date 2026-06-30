from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dawydgawiydgaiwd qwawdaiwadawd'


    from app.auth.routes import auth
    from app.dashboard.routes import views

    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(views, url_prefix="/")

    return app