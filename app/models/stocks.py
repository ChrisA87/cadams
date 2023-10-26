from datetime import datetime, timedelta, date
import pandas_datareader as pdr
import yfinance as yf
import pandas as pd
from pandas import MultiIndex
from sqlalchemy import func
from .. import db
from ..utils import to_json_safe


STARTING_STOCKS = [
    ('AAPL', 'Apple, Inc.'),
    ('MSFT', 'Microsoft Corporation'),
    ('AMZN', 'Amazon.com, Inc.'),
    ('EURUSD=X', 'Euro / US Dollar Rate'),
    ('GDX', 'VanEck Gold Miners ETF'),
    ('GLD', 'SPDR Gold Trust'),
    ('META', 'Meta Platforms, Inc.'),
    ('CNA.L', 'Centrica plc'),
    ('SONY', 'Sony Group Coropration'),
    ('TTWO', 'Take-Two Interactive Software, Inc.'),
    ('NFLX', 'Netflix, Inc.'),
    ('SNOW', 'Snowflake Inc.'),
    ('VUAG.L', 'Vanguard S&P 500 ETF')
]


PORTFOLIO_STOCKS = ['META', 'CNA.L', 'AAPL', 'SONY', 'MSFT', 'TTWO', 'NFLXZ', 'SNOW', 'VUAG.L']


def get_stock_and_price_data(symbol, duration=None):
    duration = 10 if duration is None else int(duration)
    stock = Stock.query.filter_by(symbol=symbol).first_or_404()
    start_date = datetime.today() - pd.Timedelta(days=365 * duration)
    base_query = (StockPrice.query
                  .with_entities(StockPrice.date,
                                 StockPrice.adj_close)
                  .filter_by(symbol=symbol)
                  .filter(StockPrice.date >= start_date))
    prices = pd.read_sql(base_query.statement, base_query.session.bind)
    return stock, prices


class Stock(db.Model):
    __tablename__ = 'stocks'
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(64), unique=True)
    name = db.Column(db.String(64), unique=True)
    last_updated = db.Column(db.DateTime())

    @staticmethod
    def insert_stocks(stocks=STARTING_STOCKS):
        for symbol, name in stocks:
            stock = Stock.query.filter_by(symbol=symbol).first()
            if stock is None:
                stock = Stock(symbol=symbol, name=name, last_updated=None)
                db.session.add(stock)
                db.session.commit()

    def update(self):
        if self.last_updated is None or self.last_updated.date() < date.today():
            try:
                StockPrice.update(self.symbol)
                self.last_updated = datetime.now()
                db.session.add(self)
                db.session.commit()
            except Exception:
                # TODO - proper exception handling and logging here
                pass

    def to_dict(self, *exclude_keys):
        return {column.name: to_json_safe(getattr(self, column.name))
                for column in self.__table__.columns}

    def __repr__(self):
        return f"<Stock[{self.id}]: {self.name} ({self.symbol})>"


class StockPrice(db.Model):
    __tablename__ = 'stock_prices'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime())
    symbol = db.Column(db.String(10), db.ForeignKey('stocks.symbol'), index=True)
    open = db.Column(db.Float)
    close = db.Column(db.Float)
    adj_close = db.Column(db.Float)
    high = db.Column(db.Float)
    low = db.Column(db.Float)
    volume = db.Column(db.Integer)

    def __repr__(self):
        return f'<StockPrice[{self.id}]: {self.symbol} - {self.date.date()}>'

    @staticmethod
    def get_latest_date(symbol=None):
        latest_date = None
        if symbol is None:
            latest_dates = (StockPrice.query
                            .with_entities(StockPrice.symbol, func.max(StockPrice.date))
                            .group_by(StockPrice.symbol)
                            .all())
            if latest_dates:
                return min([x for _, x in latest_dates])
        else:
            latest_date = (StockPrice.query
                           .filter_by(symbol=symbol)
                           .with_entities(func.max(StockPrice.date))
                           .scalar())

        if latest_date is None:
            latest_date = (datetime.now() - timedelta(days=365*10)).date()

        return latest_date

    @staticmethod
    def get_price_data(symbols, start_date):
        if symbols is None:
            symbols = [x for x, *_ in Stock.query.with_entities(Stock.symbol).all()]
        try:
            data = pdr.yahoo.daily.YahooDailyReader(symbols=symbols, start=start_date).read()
        except TypeError:
            data = yf.download(tickers=symbols, start=start_date)
        return data

    @staticmethod
    def process_price_data(data, symbol=None):
        stock_prices = []
        if isinstance(data.columns, MultiIndex):
            if symbol is not None:
                raise ValueError("symbol value is not permitted when the price dataframe is MultiIndex.")
            symbols = data.columns.levels[1]
            for symbol in symbols:
                df = (data.xs(symbol, axis=1, level=1)
                          .dropna()
                          .reset_index()
                          .assign(symbol=symbol.upper())
                          .rename(columns=lambda x: x.replace(' ', '_').lower()))
                stock_prices.extend([StockPrice(**d) for d in df.to_dict(orient='records')])
        else:
            if symbol is None:
                raise ValueError("symbol must be supplied if the DataFrame contains price data for only a single stock.")
            df = (data.dropna()
                  .reset_index()
                  .assign(symbol=symbol.upper())
                  .rename(columns=lambda x: x.replace(' ', '_').lower()))
            stock_prices.extend([StockPrice(**d) for d in df.to_dict(orient='records')])
        return stock_prices

    @staticmethod
    def insert_stock_prices(stock_prices):
        db.session.add_all(stock_prices)
        db.session.commit()

    @staticmethod
    def update(symbol=None):
        start_date = StockPrice.get_latest_date(symbol) + timedelta(days=1)
        new_data = StockPrice.get_price_data(symbol, start_date)
        stock_prices = StockPrice.process_price_data(new_data, symbol=symbol)
        StockPrice.insert_stock_prices(stock_prices)

    def to_dict(self):
        return {column.name: to_json_safe(getattr(self, column.name))
                for column in self.__table__.columns}
