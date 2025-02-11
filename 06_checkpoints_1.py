"""
Checkpoints:
A checkpoint is a snapshot of the graph state saved at each 'super-step' (yet
to be defined)
- It is represented as a MemorySaver object
- To use the checkpointer, just pass it to the compile() function when compiling
    the graph.

StateSnapshot object has the following attributes
- config
- metadata
- values
- next
- tasks*

tasks:- A tuple of 'PregelTask' objects that contain information about subsequent
tasks.

Notes:
1. In the State object, the class attribute 'foo' is initialized as an int type.
But the nodes created afterwards override this into a string type. I'm not sure
why langchain's documentation decided to do it like this.
"""

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from typing import Annotated
from typing_extensions import TypedDict
from operator import add
from IPython.display import Image, display
import utils

class State(TypedDict):
    foo: int
    bar: Annotated[list[str], add]

def node_a(state: State):
    return {"foo": "a", "bar": ["a"]}

def node_b(state: State):
    return {"foo": "b", "bar": ["b"]}

workflow = StateGraph(State)
workflow.add_node(node_a)
workflow.add_node(node_b)
workflow.add_edge(START, "node_a")
workflow.add_edge("node_a", "node_b")
workflow.add_edge("node_b", END)

checkpointer = MemorySaver()
graph = workflow.compile(checkpointer=checkpointer)

config = {"configurable": {"thread_id": "1"}}
result = graph.invoke({"foo": ""}, config)

print(result)

# save graph
utils.save_graph("graph.png", graph)