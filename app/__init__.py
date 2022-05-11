from flask import Flask
from .main import main
from config import config


def create_app(config_name='default'):

    app = Flask(__name__)

    # Configure
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Register Blueprints
    app.register_blueprint(main)

    return app
