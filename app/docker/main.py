import pandas as pd
import datetime as dt
#from sqlalchemy import create_engine
from app.config import TODAY, BOOKS_PATH, CUSTOMERS_PATH, BOOKS_TABLE_NAME, CUSTOMERS_TABLE_NAME, CONNECTION_STRING, SAVE_TO_SQL
from loguru import logger
from app.monitoring import pipeline_metrics
import time

## Functions 
def create_dataframe(path):
    ''' 
    This function creates a pandas dataframe 
    '''

    return pd.read_csv(path)


def convert_columns_to_int(df, column_name):
    '''
    converts column to integer
    '''
    df[column_name] = pd.to_numeric(df[column_name], errors='coerce').astype('Int64')

    return df


def drop_nulls(df):
    '''
    drop rows where all values are null
    '''
    df.dropna(how='all', inplace=True)

    return df 


def keep_values_only(df, column_name):
    df[column_name] = df[column_name].astype(str).str.extract(r'(\d+)', expand=False).astype('Int64')

    return df


def rename_columns(df, columns_mapping: dict):
    return df.rename(columns=columns_mapping)


def convert_and_validate_dates(df, date_cols: list, format: str = "%d/%m/%Y"):

    # Convert date columns
    for col in date_cols:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace('"', '', regex=False)
        )

        df[col] = pd.to_datetime(
            df[col],
            format=format,
            errors="coerce"
        )
    
    return df 


def save_df_to_sql(df, table_name, conn_string, if_exists='append'):

    engine = create_engine(conn_string)

    df.to_sql(
        table_name,
        con=engine,
        if_exists = if_exists,
        index = False
    )

    return True


def enrich_date(df, start_col, end_col):

    date_difference = df[end_col] - df[start_col]
    date_difference_days = date_difference.dt.days

    return date_difference_days

## create function to monitor invalid dfs


if __name__=='__main__':

    logger.info('Cleaning process begining')
    start_time = time.time()

    # Create Dataframes
    df_books = create_dataframe(BOOKS_PATH)
    df_customers = create_dataframe(CUSTOMERS_PATH)

    number_of_inputs = len(df_books) + len(df_customers)
    pipeline_metrics['number_of_records_input'] = number_of_inputs

    ## Data Cleaning Steps

    ## convert columns to int
    df_books = convert_columns_to_int(df_books, 'Customer ID')
    df_books = convert_columns_to_int(df_books, 'Id')
    df_customers = convert_columns_to_int(df_customers, 'Customer ID')

    ## Dropping NA's
    df_books = drop_nulls(df_books)
    df_customers = drop_nulls(df_customers)

    ## Additional steps for df_books
    df_books = keep_values_only(df_books, 'Days allowed to borrow')
    ## rename columns
    mapping = {
        'Id': 'id',
        'Books': 'books',
        'Book checkout': 'book_checkout',
        'Book Returned': 'book_returned',
        'Days allowed to borrow': 'weeks_allowed_to_borrow',
        'Customer ID': 'customer_id'
    }

    df_books = rename_columns(df_books, mapping)

    df_books = convert_and_validate_dates(df_books, ['book_checkout', 'book_returned'])
    df_books = enrich_date(df_books, 'book_checkout', 'book_returned')
    logger.info('Cleaning process complete')

    number_of_outputs = len(df_books) + len(df_customers)
    pipeline_metrics['number_of_records_output'] = number_of_outputs
    pipeline_metrics['number_of_records_dropped'] = (pipeline_metrics['number_of_records_input'] - pipeline_metrics['number_of_records_output'] )

    
    pipeline_metrics['number_of_books'] = df_books['id'].unique()
    pipeline_metrics['number_of_customers'] = df_customers['customer_id'].unique()
  
    if SAVE_TO_SQL:
        logger.info('Uploading to SQL')
        save_df_to_sql(df_books, BOOKS_TABLE_NAME, CONNECTION_STRING, if_exists='append')
        save_df_to_sql(df_customers, CUSTOMERS_TABLE_NAME, CONNECTION_STRING, if_exists='append')
    

    pipeline_metrics['pipeline_execution_time'] = (round(time.time() - start_time, 2))
    metrics_df = pd.DataFrame([pipeline_metrics])
    
    metrics_df.to_csv('pipeline_metrics.csv', index=False)
    logger.info('process complete')
    




    
