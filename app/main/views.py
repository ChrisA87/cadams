import pandas as pd
from flask import render_template
from . import main
from ..models.stocks import Stock, StockPrice
from ..models.trading import SMA


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/stocks')
def stocks():
    stocks = Stock.query.all()
    return render_template('stocks.html', stocks=stocks)


@main.route('/stocks/<symbol>')
def stock_plot(symbol):
    base_query = (StockPrice.query
                  .with_entities(StockPrice.date,
                                 StockPrice.adj_close)
                  .filter_by(symbol=symbol))
    df = pd.read_sql(base_query.statement, base_query.session.bind)
    sma = SMA(df)
    sma.fit()
    script, div = sma.get_bokeh_components()
    return render_template('stock_plot.html', script=script, div=div, symbol=symbol)
