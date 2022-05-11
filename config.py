from pydantic import BaseSettings


class Config(BaseSettings):
    # TODO
    pass


class DevConfig(Config):
    # TODO
    pass


class TestConfig(Config):
    # TODO
    pass


class ProdConfig(Config):
    # TODO
    pass


config = {
    'dev': DevConfig(),
    'test': TestConfig(),
    'prod': ProdConfig(),

    'default': DevConfig()
}
