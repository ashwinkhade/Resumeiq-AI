"""
Flask extension instances.

These are created here (uninitialized) and bound to the app
in the application factory (app/__init__.py). Keeping them here
avoids circular imports between models, routes, and the factory.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()
limiter = Limiter(key_func=get_remote_address)
