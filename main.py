#import packages
import pandas as pd

# functions
def create_df(path):
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


def convert_to_dates(df, column_name, date_format):

    df[column_name] = pd.to_datetime(df[column_name], format=date_format, errors='coerce')

    return df 

def rename_columns(df, exist_column, new_column):
    return df.rename({exist_column: new_column}, inplace=True)