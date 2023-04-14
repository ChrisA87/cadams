from flask_restx import Namespace, fields

api = Namespace('Trading Models')


sma_params = api.model('ParamsSMA', {
    'fast': fields.Integer(
        example=42,
        description='Fast moving average'),
    'slow': fields.Integer(
        example=252,
        description='Slow moving average')})
