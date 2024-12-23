import pandas as pd
from sqlalchemy import create_engine, inspect
from dotenv import load_dotenv, find_dotenv
from langchain_community.utilities import SQLDatabase

# Step 0: load environment variables
_ = load_dotenv(find_dotenv())

# Step 1: Load dataset as pandas dataframe
data_path = 'titanic.csv'
df = pd.read_csv(data_path)

# Step 2: Convert Dataframe into SQL table
# Step 2.1: Create SQL engine
db_name = 'titanic'
engine = create_engine(f"sqlite:///{db_name}.db")

# Step 2.2: Write csv into sql table
inspector = inspect(engine)
if db_name in inspector.get_table_names():
    print(f"Table {db_name} already exists. Data not written to database.")
else:
    # Write to SQL database only if table doesn't exist
    df.to_sql(db_name, engine, index=False)
    print("Data written to the database.")

# Step 3: Load database
db = SQLDatabase(engine)
print(db.dialect)
print(db.get_usable_table_names())

# Step 4: Query the data
print(db.run("SELECT * FROM titanic WHERE Age <2;"))

