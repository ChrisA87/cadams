import pytest
import random
from datetime import datetime, timedelta
from app import create_app, db
from app.models.users import User
from app.models.roles import Role
from app.models.stocks import Stock, StockPrice, starting_stocks


@pytest.fixture(scope='module')
def app():
    app = create_app('test')
    app.config["TESTING"] = True
    app.app_context().push()
    yield app


@pytest.fixture(scope='module')
def client(app):
    yield app.test_client(use_cookies=True)


@pytest.fixture(scope='module')
def list_users():
    yield [
        User(username='John', email='john@example.com', password='cat', id=1),
        User(username='Susan', email='susan@example.com', password='dog', id=2),
        User(username='Bob', email='bob@example.com', password='rabbit', id=3)
    ]


@pytest.fixture(scope='module')
def list_stocks():
    yield [
        Stock(symbol='CADM', name='Cadams, Inc.'),
    ]


@pytest.fixture(scope='module')
def list_stock_prices():
    n = 10
    start_date = datetime(2022, 1, 1)
    random.seed(1234)
    yield [
        StockPrice(
            date=start_date + timedelta(days=i),
            symbol='CADM',
            open=random.random() * 10,
            close=random.random() * 10,
            adj_close=random.random() * 10,
            high=random.random() * 10,
            low=random.random() * 10
        )
        for i in range(10)
    ]


@pytest.fixture(scope='module')
def test_db(app, list_users, list_stocks, list_stock_prices):
    db.create_all()

    # Import test data
    db.session.add_all(list_users)
    db.session.add_all(list_stocks)
    db.session.add_all(list_stock_prices)
    db.session.commit()
    Role.insert_roles()
    Stock.insert_stocks(starting_stocks)

    yield db
