import pytest
from app.models.users import User


@pytest.fixture
def users():
    yield User(username='Bob'), User(username='Bill')


def test_cant_read_user_password(users):
    for u in users:
        with pytest.raises(AttributeError):
            u.password


def test_password_setter(users):
    u1, u2 = users
    u1.password = 'pa$$word!'
    assert u1.password_hash is not None
    assert u2.password_hash is None


def test_password_verification__correct(users):
    u1, u2 = users
    u1.password = 'pa$$word!'
    u2.password = 'secr3t'
    assert u1.verify_password('pa$$word!')
    assert u2.verify_password('secr3t')


def test_password_verification__incorrect(users):
    u1, _ = users
    u1.password = 'pa$$word!'
    assert not u1.verify_password('password!')


def test_password_salts_are_random(users):
    u1, u2 = users
    u1.password = 'cat'
    u2.password = 'cat'
    assert u1.password_hash != u2.password_hash
