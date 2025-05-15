from dotenv import find_dotenv, load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

# Step 1: load env variables
load_dotenv(find_dotenv())

# Step 2: Instantiate chat model
model = ChatOpenAI(model="gpt-3.5-turbo")

# Helper function to invoke model
def call_model(state: MessagesState):
    response = model.invoke(state["messages"])
    return {"messages": response}


# Step 3: Define graph
workflow = StateGraph(state_schema=MessagesState)
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

# Step 4: Add memory
checkpointer = MemorySaver()
graph = workflow.compile(checkpointer=checkpointer)

# Step 5: Configure
config = {"configurable": {"thread_id": "abc123"}}

# Step 6: Invoke graph
input_messsages = [HumanMessage("Hi! I'm Zayan.")]
result = graph.invoke({"messages": input_messsages}, config)

print(result)
result["messages"][-1].pretty_print()