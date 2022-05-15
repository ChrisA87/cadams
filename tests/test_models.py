import pytest
from app.models import users, roles


def test_query_user(test_db):
    u = users.User.query.filter_by(name='John').first()
    assert u.id == 1

def test_query_role(test_db):
    pass