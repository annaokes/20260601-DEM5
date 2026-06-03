import datetime as dt 


## Parameters 
TODAY = dt.date.today().strftime('%d/%m/%Y')
BOOKS_PATH = '/app/data/library_systembook.csv'
CUSTOMERS_PATH = '/app/data/library_systemcustomers.csv'
BOOKS_TABLE_NAME = 'library_books'
CUSTOMERS_TABLE_NAME = 'library_customers'
CONNECTION_STRING = 'sqlite:///DE5M5_Library.db'
SAVE_TO_SQL = False
