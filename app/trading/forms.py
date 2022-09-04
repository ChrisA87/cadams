from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired


class ParamsSMA(FlaskForm):
    fast = IntegerField('Fast Moving Average', default=42, validators=[DataRequired()])
    slow = IntegerField('Slow Moving Average', default=252, validators=[DataRequired()])
    duration = SelectField('Trade duration', choices=['5Y', '10Y'], default='10Y', validators=[DataRequired()])
    submit = SubmitField('Calculate')

    def validate(self):
        super().validate()
        if self.fast.data >= self.slow.data:
            self.fast.errors.append('Fast moving average must be smaller than slow moving average')
            return False
        return True
