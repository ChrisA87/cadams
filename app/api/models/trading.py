from flask_restx import Namespace, fields

api = Namespace("Trading Models")


sma_params = api.model(
    "ParamsSMA",
    {
        "fast": fields.Integer(example=42, description="Fast moving average"),
        "slow": fields.Integer(example=252, description="Slow moving average"),
    },
)


momentum_params = api.model(
    "ParamsMomentum",
    {
        "period": fields.Integer(
            example=3, description="The number of rolling days to use as a signal."
        )
    },
)


mean_reversion_params = api.model(
    "ParamsMeanReversion",
    {
        "sma": fields.Integer(example=28, description="Simple moving average."),
        "threshold": fields.Float(
            example=3.0, description="Divergence from the mean threshold for signal."
        ),
    },
)


ols_params = api.model(
    "ParamsOLS",
    {
        "lags": fields.Integer(
            example=7, description="The number of lagged days to use for the signal."
        )
    },
)
