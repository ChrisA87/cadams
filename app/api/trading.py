import datetime
from flask_restx import Namespace, Resource
from app.models.stocks import Stock, StockPrice, get_stock_and_price_data
from app.trading.strategy import SMA, Momentum, MeanReversion, OLS
from .security import require_apikey, require_public_apikey, format_response
from .models.trading import (
    sma_params,
    momentum_params,
    mean_reversion_params,
    ols_params,
)


api = Namespace(
    name="Trading",
    description="Some endpoints for algorithmic trading.",
    path="/trading",
)


def get_strategy_suggestion(strategy, symbol, payload):
    stock, prices = get_stock_and_price_data(symbol)
    strategy = strategy(prices)
    strategy.fit(**payload)
    suggestion = strategy.df.position_term.tail(1).values[0]
    position = strategy.df.position.tail(1).values[0]
    date = datetime.date.today()

    return {
        "strategy": strategy.__class__.__name__,
        "symbol": stock.symbol,
        "date": date.isoformat(),
        "suggestion": suggestion,
        "position": {strategy.short_pos: "short", 1: "long"}.get(position),
    }


@api.route("/health")
class HealthChecks(Resource):
    def get(self):
        return {"status": "ok"}


@api.route("/stocks")
@api.doc(security="apikey")
class StocksList(Resource):
    @format_response
    @require_public_apikey
    def get(self):
        return [stock.to_dict("last_updated") for stock in Stock.query.all()]


@api.route("/stock/<symbol>")
@api.doc(security="apikey")
class StockInfo(Resource):
    @format_response
    @require_apikey
    def get(self, symbol):
        stock = Stock.query.filter_by(symbol=symbol).first()
        if stock:
            return stock.to_dict("last_updated")
        return {"symbol": symbol, "result": "not found"}


@api.route("/stock-prices/<symbol>")
@api.doc(security="apikey")
class StockPrices(Resource):
    @format_response
    @require_apikey
    def get(self, symbol):
        stock_prices = StockPrice.query.filter_by(symbol=symbol).all()
        if stock_prices:
            return [price.to_dict() for price in stock_prices]
        return {"symbol": symbol, "result": "not found"}


@api.route("/strategy/sma/<symbol>")
@api.doc(security="apikey")
class SMAStrategySuggestion(Resource):
    @format_response
    @require_public_apikey
    @api.expect(sma_params, validate=True)
    def post(self, symbol: str):
        return get_strategy_suggestion(SMA, symbol, api.payload)


@api.route("/strategy/momentum/<symbol>")
@api.doc(security="apikey")
class MomentumStrategySuggestion(Resource):
    @format_response
    @require_public_apikey
    @api.expect(momentum_params, validate=True)
    def post(self, symbol: str):
        return get_strategy_suggestion(Momentum, symbol, api.payload)


@api.route("/strategy/mean-reversion/<symbol>")
@api.doc(security="apikey")
class MeanReversionStrategySuggestion(Resource):
    @format_response
    @require_public_apikey
    @api.expect(mean_reversion_params, validate=True)
    def post(self, symbol: str):
        return get_strategy_suggestion(MeanReversion, symbol, api.payload)


@api.route("/strategy/ols/<symbol>")
@api.doc(security="apikey")
class OLSStrategySuggestion(Resource):
    @format_response
    @require_public_apikey
    @api.expect(ols_params, validate=True)
    def post(self, symbol: str):
        return get_strategy_suggestion(OLS, symbol, api.payload)
