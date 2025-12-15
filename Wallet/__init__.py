from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from os import path
import os


db = SQLAlchemy()

DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'asdagasdasga'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    # Initialize db with the app
    db.init_app(app)



    # Import the blueprints and register them
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note


    return app

def create_database(app):
    # 
    if not os.path.exists(DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

