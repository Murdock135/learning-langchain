"""This lesson covers streaming.
Note: This lesson builds on the previous lesson; 10_agent.py
- We can stream back (1) messages and (2) tokens
"""

from langchain_anthropic import ChatAnthropic
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# create search tool for chat model
search = TavilySearchResults(max_results=2)
tools = [search]

# Instantiate chat model and bind search tool
model = ChatOpenAI(model="gpt-3.5-turbo")
model_with_tools = model.bind_tools(tools)

# Create Agent
agent_executor = create_react_agent(model, tools)

# Invoke agent and stream messages
prompt = "What's the weather in Columbia, Missouri?"
for chunk in agent_executor.stream({"messages": [HumanMessage(content=prompt)]}):
    print(chunk)
    print("----")
