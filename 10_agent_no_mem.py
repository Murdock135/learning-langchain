"""This lesson covers creating an agent.
Keynotes:
1. Use create_react_agent(model, tools) (from langgraph.prebuilt)
2. An agent is by default memoryless.
*. We can equip agents with tools e.g. TavilySearch for browsing the web. 
"""

from langchain_anthropic import ChatAnthropic
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import code

# create search tool for chat model (In this case TavilySearch)
search = TavilySearchResults(max_results=2)
tools = [search]

# Instantiate chat model and bind search tool
model = ChatOpenAI(model="gpt-3.5-turbo")
model_with_tools = model.bind_tools(tools)

# Create Agent
agent_executor = create_react_agent(model, tools)

# Invoke agent
prompt = "What's the weather in Columbia, Missouri?"
response = agent_executor.invoke({"messages": [HumanMessage(content=prompt)]})

for message in response['messages']:
    message.pretty_print()
# Drop into an interactive shell with access to local variables
# code.interact(local=locals())