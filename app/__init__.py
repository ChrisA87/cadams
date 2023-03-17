from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension
from config import config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
toolbar = DebugToolbarExtension()


def create_app(config_name='default'):

    app = Flask(__name__)

    # Configure
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    toolbar.init_app(app)

    # Set up admin page
    admin = Admin(template_mode='bootstrap3', url='/auth/admin')
    admin.init_app(app)
    from .models import users, stocks
    from .auth.admin import AdminModelView
    admin.add_view(AdminModelView(users.User, db.session))
    admin.add_view(AdminModelView(stocks.Stock, db.session))
    admin.add_view(AdminModelView(stocks.StockPrice, db.session))

    # Register Blueprints
    from .main import main
    app.register_blueprint(main)
    from .auth import auth
    app.register_blueprint(auth)
    from .trading import trading
    app.register_blueprint(trading)

    return app
