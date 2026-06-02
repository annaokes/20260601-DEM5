import pandas as pd
import datetime as dt
from sqlalchemy import create_engine
from config import TODAY, BOOKS_PATH, CUSTOMERS_PATH 

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


def convert_and_validate_dates(df, date_cols: list, format: str = "%d/%m/%Y" ):

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

    # Create Dataframes
    df_books = create_dataframe(BOOKS_PATH)
    df_customers = create_dataframe(CUSTOMERS_PATH)

    ## Data Cleaning Steps
    
