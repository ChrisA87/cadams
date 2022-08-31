from app.models.roles import Role


def test_role_repr():
    role = Role(id=1, name='admin')
    assert role.__repr__() == '<Role admin (1)>'
