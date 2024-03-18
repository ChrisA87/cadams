from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension
from config import config


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
toolbar = DebugToolbarExtension()


def create_app(config_name="default"):
    from .auth import auth
    from .main import main
    from .trading import trading
    from .api import blueprint as api
    from .auth.admin import admin

    app = Flask(__name__)

    # Configure
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    toolbar.init_app(app)
    admin.init_app(app)

    # Register Blueprints
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(trading)
    app.register_blueprint(api)

    return app
