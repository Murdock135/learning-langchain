from dotenv import find_dotenv, load_dotenv
from collections.abc import Sequence
from typing_extensions import Annotated, TypedDict

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
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

# Step 3: Create prompt
system_template = "You are to answer all questions as best you can in {language}"
prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), MessagesPlaceholder("messages")]
)

# Helper function to invoke model
def call_model(state: State):
    chain = prompt_template | model
    response = chain.invoke(state)
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
input_messsages = [HumanMessage("Hi! I'm Zayan.")]
language = 'Bengali'
result = graph.invoke({"messages": input_messsages, "language": language}, config)

print(result)
result["messages"][-1].pretty_print()

# Step 7.2: Invoke graph again
input_messsages = [HumanMessage("What's my name?")]
result = graph.invoke({"messages": input_messsages}, config=config)

result["messages"][-1].pretty_print()


