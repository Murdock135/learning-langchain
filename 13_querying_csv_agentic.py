import pandas as pd

from sqlalchemy import create_engine, inspect
from dotenv import load_dotenv, find_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI

# Note: Step 0 through 3 are the same as- 12_querying_csv.py
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

# Step 4: Create SQL agent
model = ChatOpenAI(model="gpt-3.5-turbo")
agent_executor = create_sql_agent(model, db=db, agent_type="openai-tools", verbose=True)

# Step 5: Invoke agent
agent_executor.invoke({"input": "what's the average age of survivors"})


