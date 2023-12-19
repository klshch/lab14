from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import JWTManager
from config import config

from flask_bcrypt import Bcrypt

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

bcrypt = Bcrypt()

basic_auth = HTTPBasicAuth(scheme='Bearer')

def create_app(config_name="default"):
    app = Flask(__name__, instance_relative_config=False)

    app.config.from_object(config.get(config_name))

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Move scrypt initialization here
    bcrypt.init_app(app)

    JWTManager(app)

    login_manager.init_app(app)
    login_manager.login_view = "users.login"
    login_manager.login_message_category = "info"

    with app.app_context():
        from .portfolio import portfolio
        app.register_blueprint(portfolio)

        from .users import users
        app.register_blueprint(users)

        from .cookies import cookies
        app.register_blueprint(cookies)

        from .todo import todo
        app.register_blueprint(todo)

        from .control import control
        app.register_blueprint(control)

        from .posts import posts
        app.register_blueprint(posts)

        from .api import api_bp
        app.register_blueprint(api_bp)

    return app
