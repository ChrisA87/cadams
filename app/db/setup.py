import os
from app import create_app
from app.models.stocks import Stock, StockPrice
from app.models.roles import Role


def main():
    app = create_app(os.environ.get('FLASK_ENV', 'default'))
    with app.app_context():
        print('Inserting roles...', end=' ')
        Role.insert_roles()
        print('Done\nInserting starter stocks...', end=' ')
        Stock.insert_stocks()
        print('Done\nInserting stock prices...')
        StockPrice.update()
        print('Done')


if __name__ == '__main__':
    main()
