import pandas as pd
from flask import render_template
from flask_login import login_required
from . import trading
from ..models.stocks import Stock, StockPrice, starting_stocks
from . import SMA


@trading.route('/stocks')
@login_required
def stocks():
    symbols = [x for x, _ in starting_stocks]
    stocks = Stock.query.filter(Stock.symbol.in_(symbols)).all()
    return render_template('trading/stocks.html', stocks=stocks, sample=False)


@trading.route('/sample-stocks')
def sample_stocks():
    symbols = [x for x, _ in starting_stocks]
    stocks = Stock.query.filter(Stock.symbol.in_(symbols)).all()
    return render_template('trading/stocks.html', stocks=stocks, sample=True)


@trading.route('/stocks/<symbol>')
def stock_page(symbol):
    stock = Stock.query.filter_by(symbol=symbol).first_or_404()
    return render_template('trading/stock_page.html', stock=stock)


@trading.route('/stocks/<symbol>/<strategy>')
def stock_plot(symbol, strategy):
    stock = Stock.query.filter_by(symbol=symbol).first_or_404()
    base_query = (StockPrice.query
                  .with_entities(StockPrice.date,
                                 StockPrice.adj_close)
                  .filter_by(symbol=symbol))
    df = pd.read_sql(base_query.statement, base_query.session.bind)
    sma = SMA(df)
    sma.fit()
    script, div = sma.get_bokeh_components(stock)
    return render_template('trading/stock_plot.html', script=script, div=div, stock=stock, strategy=strategy)
