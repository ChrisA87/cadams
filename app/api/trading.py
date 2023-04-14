import datetime
from flask_restx import Namespace, Resource
from app.models.stocks import Stock, StockPrice, get_stock_and_price_data
from app.trading.strategy import SMA
from .security import require_apikey, require_public_apikey, format_response
from .models.trading import sma_params


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


@api.route("/strategy/sma/<symbol>")
@api.route("/strategy/sma/<symbol>/<date>")
@api.doc(security='apikey')
class SMAStrategySuggestion(Resource):
    @format_response
    @require_public_apikey
    @api.expect(sma_params, validate=True)
    def post(self, symbol: str, date: datetime.date = None):
        stock, prices = get_stock_and_price_data(symbol)
        strategy = SMA(prices)
        strategy.fit(**api.payload)
        if date is None:
            suggestion = strategy.df.position_term.tail(1).values[0]
            position = strategy.df.position.tail(1).values[0]
            date = datetime.date.today().isoformat()
        else:
            suggestion = strategy.df.loc[date, 'position_term'].values[0]
            position = strategy.df.loc[date, 'position'].values[0]
        return {
            'strategy': 'SMA',
            'symbol': stock.symbol,
            'date': date,
            'suggestion': suggestion,
            'position': {strategy.short_pos: 'short', 1: 'long'}.get(position)}
