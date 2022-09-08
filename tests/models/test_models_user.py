import pytest


def test_cant_read_user_password(list_users):
    for u in list_users:
        with pytest.raises(AttributeError):
            u.password


def test_password_setter(list_users):
    u1, *_ = list_users
    u1.password = 'pa$$word!'
    assert u1.password_hash is not None


def test_password_verification__correct(list_users):
    u1, u2, _ = list_users
    u1.password = 'pa$$word!'
    u2.password = 'secr3t'
    assert u1.verify_password('pa$$word!')
    assert u2.verify_password('secr3t')


def test_password_verification__incorrect(list_users):
    u1, *_ = list_users
    u1.password = 'pa$$word!'
    assert not u1.verify_password('password!')


def test_password_salts_are_random(list_users):
    u1, u2, _ = list_users
    u1.password = 'cat'
    u2.password = 'cat'
    assert u1.password_hash != u2.password_hash


def test_confirm_verify_token__valid(app, list_users):
    u1, *_ = list_users
    token = u1.generate_verify_token()
    assert u1.confirm(token)


def test_confirm_verify_token__invalid(app, list_users):
    u1, u2, _ = list_users
    u1_token = u1.generate_verify_token()
    assert not u2.confirm(u1_token)


def test_confirm_exception(app, list_users):
    u1, *_ = list_users
    assert not u1.confirm(None)


def test_user_repr(app, list_users):
    u1, *_ = list_users
    assert u1.__repr__() == '<User John (1)>'
