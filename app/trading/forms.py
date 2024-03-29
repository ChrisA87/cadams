from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, SelectField, FloatField
from wtforms.validators import DataRequired


class ParamsBase(FlaskForm):
    """Base parameters common to all trading strategies."""
    duration = SelectField('Trade duration (years)', choices=[5, 10], default=10, validators=[DataRequired()])
    submit = SubmitField('Calculate')


class ParamsSMA(ParamsBase):
    """Simple Moving Average trading strategy parameters."""
    fast = IntegerField('Fast Moving Average', default=42, validators=[DataRequired()])
    slow = IntegerField('Slow Moving Average', default=252, validators=[DataRequired()])

    def validate(self, extra_validators=None):
        super().validate(extra_validators=extra_validators)
        if self.fast.data >= self.slow.data:
            self.fast.errors.append('Fast moving average must be smaller than slow moving average')
            return False
        return True


class ParamsMomentum(ParamsBase):
    """Momentum trading strategy parameters"""
    period = IntegerField('Period', default=3, validators=[DataRequired()])


class ParamsMeanReversion(ParamsBase):
    """Mean Reversion trading strategy parameters."""
    sma = IntegerField('Simple Moving Average', default=28, validators=[DataRequired()])
    threshold = FloatField('Threshold', default=3.0, validators=[DataRequired()])


class ParamsOLS(ParamsBase):
    """OLS trading strategy parameters."""
    lags = IntegerField('Lags', default=7, validators=[DataRequired()])
