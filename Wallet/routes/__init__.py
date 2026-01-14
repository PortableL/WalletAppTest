from flask import Flask
import os
from ..extensions import db, migrate, login_manager


def create_app():
    
    app = Flask(__name__, 
            template_folder='../templates',  # Point to templates folder
            static_folder='../static')  
    
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "your_default_secret_key")

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        "DATABASE_URL",
        "postgresql+psycopg://neondb_owner:PASSWORD@"
        "ep-shy-fog-a1pefib0-pooler.ap-southeast-1.aws.neon.tech/"
        "neondb?sslmode=require&channel_binding=require"
    )

    # Recommended settings
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Fixed typo
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "pool_pre_ping": True,
    }

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models (UPDATED PATH)
    from ..models.user import User, Note
    from ..models.wallet import Wallet, Transaction
    # Add inventory models when ready:
    # from ..models.inventory import Inventory, Item

    # Register blueprints (UPDATED)
    from .auth import auth
    from .wallet import wallet_bp
    from .inventory import inventory_bp
    from .savings import savings_bp
    
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(wallet_bp, url_prefix='/wallet')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
    app.register_blueprint(savings_bp, url_prefix='/savings')

    # Initialize Flask-Login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # ✅ ADD THIS SECTION - Prevent caching of protected pages
    @app.after_request
    def add_security_headers(response):
        # Prevent caching
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response

    return app