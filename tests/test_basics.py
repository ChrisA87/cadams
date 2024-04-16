from flask import current_app


def test_app_config_exists(app):
    assert current_app is not None


def test_app_config_is_testing(app):
    assert current_app.config["TESTING"]
