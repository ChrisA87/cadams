from datetime import datetime
import pandas as pd
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from . import trading, SMA
from .forms import ParamsSMA
from ..models.stocks import Stock, StockPrice, starting_stocks


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


@trading.route('/stocks/<symbol>/simple-moving-average', methods=['GET', 'POST'])
def strategy_sma(symbol):
    form = ParamsSMA()
    fast = 42
    slow = 252
    duration = '10Y'

    if request.method == 'POST':
        if form.validate_on_submit():
            fast = form.fast.data
            slow = form.slow.data
            duration = form.duration.data
        else:
            flash('invalid input')
            redirect(url_for('trading.strategy_sma', symbol=symbol))

    stock = Stock.query.filter_by(symbol=symbol).first_or_404()
    start_date = datetime.today() - pd.Timedelta(duration)
    base_query = (StockPrice.query
                  .with_entities(StockPrice.date,
                                 StockPrice.adj_close)
                  .filter_by(symbol=symbol)
                  .filter(StockPrice.date >= start_date))
    df = pd.read_sql(base_query.statement, base_query.session.bind)
    sma = SMA(df, short_pos=-1)
    sma.fit(fast=fast, slow=slow)
    returns = sma.get_returns().to_dict()
    returns_script, returns_div = sma.get_returns_plot_components(stock)
    sma_script, sma_div = sma.get_sma_plot_components(stock)
    return render_template('trading/strategy_sma.html', returns_script=returns_script, returns_div=returns_div, stock=stock,
                           form=form, sma=sma, returns=returns, sma_script=sma_script, sma_div=sma_div)
