from .. import db

starting_stocks = [
    ('FB', 'Facebook, Inc.'),
    ('AAPL', 'Apple, Inc.'),
    ('SONY', 'Sony Group Corporation'),
    ('MSFT', 'Microsoft Corporation'),
    ('TTWO', 'Take-Two Interactive Software, Inc.'),
    ('NFLX', 'Netflix, Inc.'),
    ('SNOW', 'Snowflake, Inc.')
]


class Stock(db.Model):
    __tablename__ = 'stocks'
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(64), unique=True)
    name = db.Column(db.String(64), unique=True)

    @staticmethod
    def insert_stocks(stocks=starting_stocks):
        for symbol, name in stocks:
            stock = Stock.query.filter_by(symbol=symbol).first()
            if stock is None:
                stock = Stock(symbol=symbol, name=name)
                db.session.add(stock)
                db.session.commit()

    def __repr__(self):
        return f"<Stock [{self.id}]: {self.name} ({self.symbol})>"


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
        return f'<StockPrice[{self.id}]: {self.symbol} - {self.date}>'