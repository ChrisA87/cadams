from flask_wtf import FlaskForm
from pydantic import ValidationError
from wtforms import StringField, SubmitField, PasswordField, BooleanField, EmailField
from wtforms.validators import DataRequired, Length, Regexp, Email, EqualTo
from ..models.users import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(3, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Length(3, 64), Email()])
    username = StringField('Username', validators=[
        DataRequired(),
        Length(3, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_]*$', 0, 'Usernames can only contain letters, numbers or underscores.')])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo(password, 'Passwords must match')])
    not_a_robot = BooleanField('I am not a robot')
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email alread registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already taken.')
