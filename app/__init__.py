from flask import Flask
from flask_bootstrap import Bootstrap
from .main import main
from config import config

bootstrap = Bootstrap()


def create_app(config_name='default'):

    app = Flask(__name__)

    # Configure
    app.config.from_object(config[config_name])

    # Initiate extensions
    bootstrap.init_app(app)

    # Register Blueprints
    app.register_blueprint(main)

    return app
