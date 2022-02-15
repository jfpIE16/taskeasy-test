"""Data Replication Script

This script allows the user to replicate a table in database A to database B.

This script requires that `pandas` and `sqlalchemy` be installed within the Python
environment you are running this script in.

Author: Fernando Pérez
Date: Mon Feb 14 18:47
"""
from sqlalchemy import create_engine, table
import pandas as pd


# Create engine for database A and B
try:
    engine_a = create_engine('sqlite:///test.db', echo=False)
    engine_b = create_engine('postgresql://test:test@localhost/test')
    print('Engines created succesfully')
    
except Exception as e:
    print(f'Error trying to create engines : {e}')
        

def replicate(table_name):
    # Replication function
    try:
        df_origin = pd.read_sql(f'SELECT * FROM {table_name}', con=engine_a)
        df_origin.to_sql(table_name, if_exists='Replace', con=engine_b)
        print('Replication successful!')
    except Exception as e:
        print(f'Error during replication: {e}')

if __name__ == '__main__':
    table_2_rep = 'table_a'
    replicate(table_name=table_2_rep)