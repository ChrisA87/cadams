from os.path import dirname, abspath
from pydantic import BaseSettings

basedir = abspath(dirname(__name__))


class Config(BaseSettings):
    SECRET_KEY: str = 'real-secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SENDGRID_API_KEY: str = 'secret-api-key'

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    FLASK_ENV: str = 'development'
    FLASK_DEBUG: bool = True
    TEMPLATES_AUTO_RELOAD: bool = True
    SQLALCHEMY_DATABASE_URI: str = f'sqlite:///{basedir}/data-dev.sqlite'


class TestConfig(Config):
    FLASK_ENV: str = 'testing'
    TESTING: bool = True
    SQLALCHEMY_DATABASE_URI: str = 'sqlite://'


class ProdConfig(Config):
    FLASK_ENV: str = 'production'
    SQLALCHEMY_DATABASE_URI: str = f'sqlite:///{basedir}/data.sqlite'


config = {
    'dev': DevConfig(),
    'test': TestConfig(),
    'prod': ProdConfig(),

    'default': DevConfig()
}
