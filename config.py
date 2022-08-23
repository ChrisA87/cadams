from os.path import dirname, abspath
from pydantic import BaseSettings

basedir = abspath(dirname(__file__))


class Config(BaseSettings):
    SECRET_KEY: str = 'secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SENDGRID_API_KEY: str = 'secret-api-key'

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    FLASK_ENV: str = 'development'
    FLASK_DEBUG: bool = True
    DEBUG_TB_ENABLED: bool = True
    TEMPLATES_AUTO_RELOAD: bool = True
    SQLALCHEMY_DATABASE_URI: str = f'sqlite:///{basedir}/data-dev.sqlite'


class TestConfig(Config):
    FLASK_ENV: str = 'test'
    TESTING: bool = True
    SQLALCHEMY_DATABASE_URI: str = 'sqlite://'
    WTF_CSRF_ENABLED = False


class ProdConfig(Config):
    FLASK_ENV: str = 'prod'
    SQLALCHEMY_DATABASE_URI: str = 'mysql+pymysql://root:root@172.17.0.2/cadams'
    PREFERRED_URL_SCHEME: str = 'https'


config = {
    'dev': DevConfig(),
    'test': TestConfig(),
    'prod': ProdConfig(),

    'default': DevConfig()
}
