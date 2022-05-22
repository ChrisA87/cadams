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
    def insert_roles():
        for id, (symbol, name) in enumerate(starting_stocks, 1):
            stock = Stock.query.filter_by(symbol=symbol).first()
            if stock is None:
                stock = Stock(symbol=symbol, name=name, id=id)
                db.session.add(stock)
                db.session.commit()

    def __repr__(self):
        return f"<Stock {self.symbol} - {self.name} ({self.id})>"
