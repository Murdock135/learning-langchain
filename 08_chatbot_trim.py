"""This lesson covers using a trimmer in a chatbot langgraph (a langgraph
meant to build a chatbot) to control the length of the history the model 
gets to use.

Trimmer: A trimmer allows specification of the number of tokens
we want to keep, whether the system message should be kept and 
whether partial messages should be kept.
"""

from dotenv import find_dotenv, load_dotenv
from collections.abc import Sequence
from typing_extensions import Annotated, TypedDict

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, BaseMessage, trim_messages, AIMessage, SystemMessage, trim_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph, add_messages
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Step 1: load env variables
load_dotenv(find_dotenv())

# Step 2: Instantiate chat model
model = ChatOpenAI(model="gpt-3.5-turbo")

# Step 3: Create State object
class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    language: str

# Step 3: Create trimmer
trimmer = trim_messages(
    max_tokens=65,
    strategy="last", # Keep the last '<= n_count' tokens of the messages.
    token_counter=model,
    include_system=True, # Include the system message
    allow_partial=False, # Whether to split a message if only part of the message can be included
    start_on="human", # The message type to start on. Note: Read more in function definition.
)

# Example conversation
messages = [
    SystemMessage(content="you're a good assistant"),
    HumanMessage(content="hi! I'm bob"),
    AIMessage(content="hi!"),
    HumanMessage(content="I like vanilla ice cream"),
    AIMessage(content="nice"),
    HumanMessage(content="whats 2 + 2"),
    AIMessage(content="4"),
    HumanMessage(content="thanks"),
    AIMessage(content="no problem!"),
    HumanMessage(content="having fun?"),
    AIMessage(content="yes!"),
]

# Step 4: Create prompt template
system_template = "Answer all questions as best you can in {language}"
prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), MessagesPlaceholder(variable_name="messages")]
)

# Helper function to invoke model
def call_model(state: State):
    chain = prompt_template | model
    trimmed_messages = trimmer.invoke(state["messages"])
    response = chain.invoke({"messages": trimmed_messages, "language": state["language"]})
    return {"messages": response}

# Step 4: Define graph
workflow = StateGraph(state_schema=State)
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

# Step 5: Add memory
checkpointer = MemorySaver()
graph = workflow.compile(checkpointer=checkpointer)

# Step 6: Configure
config = {"configurable": {"thread_id": "abc123"}}

# Step 7: Invoke graph
input_message = "What is my name?"
input_messages = messages + [HumanMessage(input_message)]
language = "English"
response = graph.invoke({"messages": input_messages, "language": language}, config)

response["messages"][-1].pretty_print()


