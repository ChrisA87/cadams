from flask_restx import Namespace, Resource
from .security import require_apikey, require_public_apikey, format_response
from ..models.stocks import Stock, StockPrice


api = Namespace(
    name='Trading',
    description='Some endpoints for algorithmic trading.',
    path='/trading')


@api.route("/health")
class HealthChecks(Resource):
    def get(self):
        return {"status": "ok"}


@api.route("/stocks")
@api.doc(security='apikey')
class StocksList(Resource):
    @format_response
    @require_public_apikey
    def get(self):
        return [stock.to_dict('last_updated') for stock in Stock.query.all()]


@api.route("/stock/<symbol>")
@api.doc(security='apikey')
class StockInfo(Resource):
    @format_response
    @require_apikey
    def get(self, symbol):
        stock = Stock.query.filter_by(symbol=symbol).first()
        if stock:
            return stock.to_dict('last_updated')
        return {'symbol': symbol, 'result': 'not found'}


@api.route("/stock-prices/<symbol>")
@api.doc(security='apikey')
class StockPrices(Resource):
    @format_response
    @require_apikey
    def get(self, symbol):
        stock_prices = StockPrice.query.filter_by(symbol=symbol).all()
        if stock_prices:
            return [price.to_dict() for price in stock_prices]
        return {'symbol': symbol, 'result': 'not found'}
