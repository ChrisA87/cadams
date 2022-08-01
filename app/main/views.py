import pandas as pd
from flask import render_template
from . import main
from ..models.stocks import Stock, StockPrice, starting_stocks
from ..trading import SMA


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/sample-stocks')
def stocks():
    symbols = [x for x, _ in starting_stocks]
    stocks = Stock.query.filter(Stock.symbol.in_(symbols)).all()
    return render_template('stocks.html', stocks=stocks)


@main.route('/stocks/<symbol>')
def stock_plot(symbol):
    stock = Stock.query.filter_by(symbol=symbol).first_or_404()
    base_query = (StockPrice.query
                  .with_entities(StockPrice.date,
                                 StockPrice.adj_close)
                  .filter_by(symbol=symbol))
    df = pd.read_sql(base_query.statement, base_query.session.bind)
    sma = SMA(df)
    sma.fit()
    script, div = sma.get_bokeh_components(stock)
    return render_template('stock_plot.html', script=script, div=div, symbol=symbol)
