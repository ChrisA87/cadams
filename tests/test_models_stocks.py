from datetime import datetime
from app.models.stocks import Stock, StockPrice


def test_stock_repr():
    stock = Stock(id=1, symbol='TST', name='Testing Stock')
    assert stock.__repr__() == '<Stock[1]: Testing Stock (TST)>'


def test_stock_price_repr():
    stock_price = StockPrice(id=1, symbol='TST', date=datetime(2022, 1, 1))
    assert stock_price.__repr__() == '<StockPrice[1]: TST - 2022-01-01>'
