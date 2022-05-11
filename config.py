from pydantic import BaseSettings


class Config(BaseSettings):
    # TODO
    name: str = 'common'

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    # TODO
    name: str = 'dev'


class TestConfig(Config):
    # TODO
    name: str = 'test'


class ProdConfig(Config):
    # TODO
    name: str = 'production'


config = {
    'dev': DevConfig(),
    'test': TestConfig(),
    'prod': ProdConfig(),

    'default': DevConfig()
}
