
from sqlalchemy import create_engine
import pandas as pd

# Create engine for sqlite3 database
engine = create_engine('sqlite:///taskeasy.db', echo=False)

# Read data from Excel to fill the database
products = pd.read_excel(
    'data/Data Engineer Screening Data Tables.xlsx', 
    sheet_name='Products',
    usecols=lambda x: 'id' not in x)
discounts = pd.read_excel(
    'data/Data Engineer Screening Data Tables.xlsx', 
    sheet_name='Discounts',
    usecols=lambda x: 'id' not in x)
try:
    products.to_sql('Products', con=engine, if_exists='replace', index=False)
    discounts.to_sql('Discounts', con=engine, if_exists='replace')
except Exception as e:
    print(e)

