from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired(), EqualTo('name2', message='names must match')])
    name2 = StringField('repeat', validators=[DataRequired()])
    submit = SubmitField('Submit')
