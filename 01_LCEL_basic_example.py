# Environment setup
from dotenv import load_dotenv, find_dotenv
import os

# Model imports
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv(find_dotenv())

# Initialize model and parser
model = ChatOpenAI(model="gpt-3.5-turbo")
parser = StrOutputParser()
print(help(model))

# Set up messages for translation
messages = [
    SystemMessage(content="Translate the following from English into Italian"),
    HumanMessage(content="what's up man")
]

# Execute and print translation
result = model.invoke(messages)
result_string = parser.invoke(result)
print(f"{result}\n{result_string}")

# Chain the model and parser
chain = model | parser
print(chain.invoke(messages))