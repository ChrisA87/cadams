import os
from app import create_app
from app.models.stocks import Stock, StockPrice


def main():
    app = create_app(os.environ.get('FLASK_ENV', 'default')) 
    with app.app_context():
        print('Inserting starter stocks...', end=' ')
        Stock.insert_stocks()
        print('Done\nInserting stock prices...')
        StockPrice.update()
        print('Done')


if __name__ == '__main__':
    main()
