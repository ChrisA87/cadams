import pytest
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from freezegun import freeze_time
from app.models.stocks import Stock, StockPrice


def generate_mock_price_data(symbols, start_date, periods=5):
    if isinstance(symbols, str):
        symbols = [symbols]
    metrics = ['Adj Close', 'Close', 'High', 'Low', 'Open', 'Volume']
    columns = pd.MultiIndex.from_product([metrics, symbols])
    index = pd.date_range(start=start_date, periods=periods, name='Date')
    m = len(metrics) * len(symbols)
    df = pd.DataFrame(np.random.randn(periods, m), columns=columns, index=index)
    if len(symbols) == 1:
        df = df.droplevel(1, axis=1)
    return df


def test_stock_repr():
    stock = Stock(id=1, symbol='TST', name='Testing Stock')
    assert stock.__repr__() == '<Stock[1]: Testing Stock (TST)>'


@freeze_time('2023-01-01 13:00')
def test_stock_update(monkeypatch, test_db):
    monkeypatch.setattr(StockPrice, 'update', lambda x: None)
    stock = Stock(symbol='CDMS', name='Cadams Stock')
    assert stock.last_updated is None
    stock.update()
    assert stock.last_updated == datetime(2023, 1, 1)


def test_stock_price_repr():
    stock_price = StockPrice(id=1, symbol='TST', date=datetime(2022, 1, 1))
    assert stock_price.__repr__() == '<StockPrice[1]: TST - 2022-01-01>'


def test_StockPrice_get_latest_date__symbol_none(app, test_db):
    latest = StockPrice.get_latest_date()
    expected = datetime(2023, 5, 15)
    assert latest == expected


def test_StockPrice_get_latest_date__symbol_CADM(app, test_db):
    latest = StockPrice.get_latest_date('CADM')
    expected = datetime(2023, 5, 15)
    assert latest == expected


def test_StockPrice_get_latest_date__symbol_unknown(app, test_db):
    latest = StockPrice.get_latest_date('fake')
    expected = (datetime.now() - timedelta(days=365*10)).date()
    assert latest == expected


def test_StockPrice_process_price_data__single_stock(app, test_db):
    start_date = StockPrice.get_latest_date('CADM')
    data = generate_mock_price_data('CADM', start_date)
    result = StockPrice.process_price_data(data, symbol='CADM')
    assert len(result) == 5
    assert all([isinstance(x, StockPrice) for x in result])


def test_StockPrice_process_price_data__multi_stock(app, test_db):
    start_date = StockPrice.get_latest_date('CADM')
    data = generate_mock_price_data(['CADM', 'TEST'], start_date)
    result = StockPrice.process_price_data(data)
    assert len(result) == 10
    assert all([isinstance(x, StockPrice) for x in result])


def test_StockPrice_process_price_data__multi_and_symbol_raises_ValueError(app, test_db):
    start_date = StockPrice.get_latest_date('CADM')
    data = generate_mock_price_data(['CADM', 'TEST'], start_date)
    with pytest.raises(ValueError):
        StockPrice.process_price_data(data, symbol='CADM')


def test_StockPrice_process_price_data__single_and_no_symbol_raises_ValueError(app, test_db):
    start_date = StockPrice.get_latest_date('CADM')
    data = generate_mock_price_data('CADM', start_date)
    with pytest.raises(ValueError):
        StockPrice.process_price_data(data)


def test_StockPrice_update(app, test_db, monkeypatch):
    monkeypatch.setattr(StockPrice, 'get_price_data', lambda *args, **kwargs: generate_mock_price_data(*args, **kwargs))
    prices = StockPrice.query.filter_by(symbol='CADM').all()
    StockPrice.update('CADM')
    new_prices = StockPrice.query.filter_by(symbol='CADM').all()
    assert len(new_prices) - len(prices) == 5
    assert new_prices[-1].date > prices[-1].date
