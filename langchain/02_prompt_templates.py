"""
This lesson covers 'Prompt Templates'. There are two ways (that I am aware of) 
to create a prompt template:
(1) Using the from_messages() function (EXAMPLE 1 (commented out. Uncomment to use))
(2) Using the from_template() function (EXAMPLE 2)

A caveat with using from_template() is that we cannot chain. (I think)
"""

# Environment setup
from dotenv import load_dotenv, find_dotenv
import os

# Model imports
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv(find_dotenv())

# Initialize model and parser
model = ChatOpenAI(model="gpt-3.5-turbo")
parser = StrOutputParser()

# message templates
system_template = """\
For the following review, extract the following information:

gift: Was the item purchased as a gift for someone else? \
Answer True if yes, False if not or unknown.

delivery_days: How many days did it take for the product \
to arrive? If this information is not found, output -1.

price_value: Extract any sentences about the value or price,\
and output them as a comma separated Python list.

Format the output as JSON with the following keys:
gift
delivery_days
price_value

text: {review}
"""

# EXAMPLE 1: using ChatPromptTemplate.from_messages() with a chain
# prompt_template = ChatPromptTemplate.from_messages(
#     [("system", system_template), ("user", "{review}")]
# )


# # create chain
# user_message = "I got this pen as a gift \
#     . It took 3 days to deliver. \
#         It cost 3 yuan."
# chain = prompt_template | model | parser
# response = chain.invoke({"review": user_message})
# print(response)

# EXAMPLE 2: using ChatPromptTemplate.from_template() without a chain (can be used with chain too)
user_message = "I got this pen as a gift.\
    It took 3 days to deliver.\
    It cost 3 yuan."

prompt_template = ChatPromptTemplate.from_template(system_template)
prompt = prompt_template.format_messages(review=user_message)

response = model(messages=prompt)
print(response.content)
print(type(response.content))