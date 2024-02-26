from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os.path import exists
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'brian'
    app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///C:\Users\Brian Kipsang\Desktop\database\database.db'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .models import User

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    create_database(app)

    return app

def create_database(app):
    with app.app_context():
        if not exists('website/' + DB_NAME):
            db.create_all()
            print('Database Created!')
    
