from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, PasswordField, BooleanField,
                     EmailField, ValidationError)
from wtforms.validators import DataRequired, Length, Regexp, Email, EqualTo
from ..models.users import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(3, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Length(3, 64), Email()])
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(3, 64),
            Regexp('^[A-Za-z][A-Za-z0-9_]*$', 0,
                   'Usernames can only contain letters, '
                   'numbers or underscores.')])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', 'Passwords must match')])
    password2 = PasswordField(
        'Confirm Password',
        validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email alread registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data.lower()).first():
            raise ValidationError('Username is already taken.')
