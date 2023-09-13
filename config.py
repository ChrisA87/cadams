from os.path import dirname, abspath
from pydantic_settings import BaseSettings

basedir = abspath(dirname(__file__))


class Config(BaseSettings):
    SECRET_KEY: str = 'secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SENDGRID_API_KEY: str = 'secret-api-key'
    PUBLIC_API_KEY: str = '974004f8-c594-11ed-976c-86ad6bb37ab4'
    FLASK_ADMIN_SWATCH: str = 'cerulean'

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    FLASK_ENV: str = 'development'
    FLASK_DEBUG: bool = True
    DEBUG_TB_ENABLED: bool = False
    TEMPLATES_AUTO_RELOAD: bool = True
    SQLALCHEMY_DATABASE_URI: str = f'sqlite:///{basedir}/data-dev.sqlite'


class TestConfig(Config):
    FLASK_ENV: str = 'test'
    TESTING: bool = True
    PUBLIC_API_KEY: str = 'public-test-key'
    SQLALCHEMY_DATABASE_URI: str = 'sqlite://'
    WTF_CSRF_ENABLED: bool = False


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
