from datetime import datetime
import pandas as pd
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required

from app.trading.strategy import MeanReversion, Momentum
from . import trading, SMA
from .forms import ParamsSMA, ParamsMomentum, ParamsMeanReversion
from ..models.stocks import Stock, StockPrice, starting_stocks


def get_stock_and_price_data(symbol, duration=None):
    duration = '10Y' if duration is None else duration
    stock = Stock.query.filter_by(symbol=symbol).first_or_404()
    start_date = datetime.today() - pd.Timedelta(duration)
    base_query = (StockPrice.query
                  .with_entities(StockPrice.date,
                                 StockPrice.adj_close)
                  .filter_by(symbol=symbol)
                  .filter(StockPrice.date >= start_date))
    prices = pd.read_sql(base_query.statement, base_query.session.bind)
    return stock, prices


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

    stock, prices = get_stock_and_price_data(symbol, duration)
    sma = SMA(prices, short_pos=-1)
    sma.fit(fast=fast, slow=slow)
    returns = sma.get_returns().to_dict()
    returns_script, returns_div = sma.get_returns_plot_components(stock)
    sma_script, sma_div = sma.get_sma_plot_components(stock)
    return render_template('trading/strategy_sma.html', returns_script=returns_script, returns_div=returns_div, stock=stock,
                           form=form, sma=sma, returns=returns, sma_script=sma_script, sma_div=sma_div)


@trading.route('/stocks/<symbol>/momentum', methods=['GET', 'POST'])
def strategy_momentum(symbol):
    form = ParamsMomentum()
    period = 3
    duration = '10Y'

    if request.method == 'POST':
        if form.validate_on_submit():
            period = form.period.data
            duration = form.duration.data
        else:
            redirect(url_for('trading.strategy_momentum', symbol=symbol))

    stock, prices = get_stock_and_price_data(symbol, duration)
    momentum = Momentum(prices, short_pos=-1)
    momentum.fit(period=period)
    returns = momentum.get_returns().to_dict()
    returns_script, returns_div = momentum.get_returns_plot_components(stock)
    return render_template('trading/strategy_momentum.html', returns_script=returns_script, returns_div=returns_div,
                           stock=stock, form=form, momentum=momentum, returns=returns)


@trading.route('/stocks/<symbol>/mean-reversion', methods=['GET', 'POST'])
def strategy_mean_reversion(symbol):
    form = ParamsMeanReversion()
    sma = 25
    threshold = 3.5
    duration = '10Y'

    if request.method == 'POST':
        if form.validate_on_submit():
            sma = form.sma.data
            threshold = form.threshold.data
            duration = form.duration.data
        else:
            redirect(url_for('trading.strategy_mean_reversion', symbol=symbol))

    stock, prices = get_stock_and_price_data(symbol, duration)
    mean_rev = MeanReversion(prices, short_pos=-1)
    mean_rev.fit(sma=sma, threshold=threshold)
    returns = mean_rev.get_returns().to_dict()
    returns_script, returns_div = mean_rev.get_returns_plot_components(stock)
    distance_script, distance_div = mean_rev.get_distance_plot_components(stock)
    return render_template('trading/strategy_mean_reversion.html', returns_script=returns_script, returns_div=returns_div,
                           stock=stock, form=form, mean_rev=mean_rev, returns=returns, distance_script=distance_script,
                           distance_div=distance_div)
