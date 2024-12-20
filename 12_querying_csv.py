import pandas as pd
from sqlalchemy import create_engine, inspect
from dotenv import load_dotenv, find_dotenv
import os

_ = load_dotenv(find_dotenv())

# Load dataset as pandas dataframe
data_path = 'titanic.csv'
df = pd.read_csv(data_path)

# Create SQL engine
engine = create_engine("sqlite:///titanic.db")

# Load csv as sql table
inspector = inspect(engine)
if "titanic" in inspector.get_table_names():
    print("Table 'titanic' already exists. Data not written to database.")
else:
    # Write to SQL database only if table doesn't exist
    df.to_sql("titanic", engine, index=False)
    print("Data written to the database.")

