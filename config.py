from pydantic import BaseSettings


class Config(BaseSettings):
    SECRET_KEY: str = 'real-secret-key'

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    FLASK_ENV: str = 'development'
    FLASK_DEBUG: bool = True
    TEMPLATES_AUTO_RELOAD: bool = True


class TestConfig(Config):
    FLASK_ENV: str = 'testing'
    TESTING: bool = True


class ProdConfig(Config):
    FLASK_ENV: str = 'production'


config = {
    'dev': DevConfig(),
    'test': TestConfig(),
    'prod': ProdConfig(),

    'default': DevConfig()
}
