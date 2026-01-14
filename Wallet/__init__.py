from .extensions import db, migrate, login_manager
from .routes import create_app
__version__ = '1.0.0'
__all__ = ['db', 'migrate', 'login_manager', 'create_app']