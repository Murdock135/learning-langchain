from dotenv import find_dotenv, load_dotenv
from utils import save_graph

from langchain_openai.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage, AnyMessage, AIMessage
from langgraph.graph.message import add_messages
from langgraph.graph import MessagesState, StateGraph, START, END

from typing_extensions import TypedDict
from typing import Annotated

# load env variables
load_dotenv(find_dotenv())

# Create tool (In this case, a function)
def multiply(a, b):
    return a * b

# Create model and bind tool to model
model = ChatOpenAI(model="gpt-3.5-turbo")
model = model.bind_tools([multiply])

# Create node with the model (Node needs to be a Runnable; in this case, a function)
def call_model(state: MessagesState):
    return {"messages": model.invoke(state["messages"])}

# Build graph
workflow = StateGraph(MessagesState)
workflow.add_node("model", call_model)
workflow.add_edge(START, "model")
workflow.add_edge("model", END)
graph = workflow.compile()

# save graph
graph_save_path = "graph_lesson_09.png"
save_graph(graph_save_path, graph)

# Create conversation
messages = [HumanMessage(content="Hi"),
            AIMessage(content="Hello"),
            HumanMessage(content="multiply 2 and 3")]

response = graph.invoke({"messages": messages}) # The content of the response will be an empty string

for message in response['messages']:
    message.pretty_print()