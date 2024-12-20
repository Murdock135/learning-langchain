import pandas as pd

from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

# load dataset as pandas dataframe
data_path = 'titanic.csv'
df = pd.read_csv(data_path)

# Create SQL engine
engine = create_engine("sqlite:///titanic.db")
df.to_sql("titanic", engine, index=False)

