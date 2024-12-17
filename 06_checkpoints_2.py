from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from pydantic import BaseModel, conlist
from typing import List

# Define the state using a Pydantic model
class State(BaseModel):
    count: int
    messages: conlist(str, min_length=1) 

# Define node functions
def node_increment(state: State) -> State:
    # Increment the count and add a message
    new_count = state.count + 1
    new_messages = state.messages + [f"Incremented to {new_count}"]
    return State(count=new_count, messages=new_messages)

def node_reset(state: State) -> State:
    # Reset the count and add a reset message
    return State(count=0, messages=state.messages + ["Reset to 0"])

# Create the workflow
workflow = StateGraph(State)
workflow.add_node(node_increment)
workflow.add_node(node_reset)
workflow.add_edge(START, "node_increment")
workflow.add_edge("node_increment", "node_reset")
workflow.add_edge("node_reset", END)

# Set up checkpointing
checkpointer = MemorySaver()
graph = workflow.compile(checkpointer=checkpointer)

# Invoke the graph with initial state
initial_state = State(count=0, messages=["Starting the process"])
config = {"configurable": {"thread_id": "1"}}
result = graph.invoke(initial_state.dict(), config)

# Print the result
print(result)
