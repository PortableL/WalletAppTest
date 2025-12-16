from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from os import path
import os
from flask_migrate import Migrate
from flask_login import LoginManager

migrate = Migrate()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "your_default_secret_key") #Secret key


    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        "DATABASE_URL",
        "postgresql+psycopg://neondb_owner:PASSWORD@"
        "ep-shy-fog-a1pefib0-pooler.ap-southeast-1.aws.neon.tech/"
        "neondb?sslmode=require&channel_binding=require"
    )

    #Recommended settings
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_pre_ping": True,
    } # prevents stale connection errors


    # Initialize db with the app
    db.init_app(app)
    migrate.init_app(app, db)



    # Import the blueprints and register them
    from .views import views
    from .auth import auth
    from .models import User, Note

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


    return app


