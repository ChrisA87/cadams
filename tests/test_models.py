from xml.dom.minidom import Attr
import pytest
from app.models import users, roles


def test_query_user(test_db):
    u = users.User.query.filter_by(name='John').first()
    assert u.id == 1

def test_cant_read_user_password(test_db):
    u = users.User.query.filter_by(name='John').first()
    with pytest.raises(AttributeError):
        u.password

def test_password_setter():
    u = users.User(name='Steve')
    u.password = 'pa$$word!'
    assert u.password_hash is not None

def test_password_verification__correct():
    u = users.User(name='Steve')
    u.password = 'pa$$word!'
    assert u.verify_password('pa$$word!')

def test_password_verification__incorrect():
    u = users.User(name='Steve')
    u.password = 'pa$$word!'
    assert not u.verify_password('password!')

def test_password_salts_are_random():
    u1 = users.User(name='Bob', password='cat')
    u2 = users.User(name='Bill', password='cat')
    assert u1.password_hash != u2.password_hash
