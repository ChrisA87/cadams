from flask import current_app
from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous.url_safe import URLSafeSerializer
from flask_login import UserMixin
from .. import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    created = db.Column(db.DateTime())
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), default=1)
    api_key = db.Column(db.String(64))
    confirmed = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError('Password is not a readable field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_verify_token(self):
        s = URLSafeSerializer(current_app.config['SECRET_KEY'], salt='verify')
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = URLSafeSerializer(current_app.config['SECRET_KEY'], salt='verify')
        try:
            data = s.loads(token)
        except Exception:
            return False
        if data.get('confirm') != self.id:
            return False
        self.verified = True
        db.session.add(self)
        return True

    def __repr__(self):
        return f'<User {self.username} ({self.id})>'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
