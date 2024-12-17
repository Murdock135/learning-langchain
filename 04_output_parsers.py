"""
This lesson covers creating output parsers and then using it. To create an output parser,
1. We use from_response_schemas() from the StructuredOutputParser module.
2. from_response_schemas() takes a list of ResponseSchema objects.
3. Get formatting instructions using get_format_instructions(), a method withing StructuredOutputParser.
4. Use the formatting instructions in the system template (refer to lesson 02 to know more about system templates)
"""

# Environment setup
from dotenv import load_dotenv, find_dotenv
import os

# Model imports
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser

# Load environment variables
load_dotenv(find_dotenv())

# 1. create model
model = ChatOpenAI(model="gpt-3.5-turbo")

# 2. create output parser (OOP would be better)
gift_schema = ResponseSchema(name="gift",
                             description="Was the item purchased\
                             as a gift for someone else? \
                             Answer True if yes,\
                             False if not or unknown.")
delivery_days_schema = ResponseSchema(name="delivery_days",
                                      description="How many days\
                                      did it take for the product\
                                      to arrive? If this \
                                      information is not found,\
                                      output -1.")
price_value_schema = ResponseSchema(name="price_value",
                                    description="Extract any\
                                    sentences about the value or \
                                    price, and output them as a \
                                    comma separated Python list.")

response_schemas = [gift_schema, 
                    delivery_days_schema,
                    price_value_schema]

# 3. create format instructions
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()
# print(format_instructions)

# 4. system message
system_template = """\
    For the following review, extract the following information:

    gift: Was the item purchased as a gift for someone else? \
    Answer True if yes, False if not or unknown.

    delivery_days: How many days did it take for the product \
    to arrive? If this information is not found, output -1.

    price_value: Extract any sentences about the value or price,\
    and output them as a comma separated Python list.

    Format the output as a python list 

    text: {review}
    {format_instructions}
    """
# Note: Note that we asked the LLM to 
# output the output as a list but it
# doesn't matter. It still outputs
# a JSON object.

# 5. user message
user_message = "I got this pen as a gift.\
    It took 3 days to deliver.\
    It cost 3 yuan."

# 6. create prompt
prompt_template = ChatPromptTemplate.from_template(system_template)
prompt = prompt_template.format_messages(review=user_message, format_instructions=format_instructions)

# 7. get response
response = model(prompt)

# 8. parse response with output parser
output_dict = output_parser.parse(response.content)
print(output_dict)
print(type(output_dict))

# 9. extract desired data (for example deliver_days)
delivery_days = output_dict.get('delivery_days')
print(delivery_days)