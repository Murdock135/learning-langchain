from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

env_path = "/home/zayan/.secrets/.llm_apis"
load_dotenv(env_path)

def get_weather(city: str) -> str:
    """Get weather for a given city"""
    return f"It's always sunny in {city}"

agent = create_react_agent(
    model="o3-mini",
    tools=[get_weather],
    prompt="You are a helpful assistant"
)

response = agent.invoke(
        {
            "messages":
                [
                    {"role": "user", "content": "What is the weather in SF?"}
                ]
        }
    )

print(response['messages'][1])