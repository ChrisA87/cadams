from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .main import main
from config import config

db = SQLAlchemy()


def create_app(config_name='default'):

    app = Flask(__name__)

    # Configure
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Initialize extensions
    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(main)

    return app
