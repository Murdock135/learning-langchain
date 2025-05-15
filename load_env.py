from dotenv import load_dotenv
import os

if __name__ == "__main__":
    env_path = "/home/zayan/.secrets/.llm_apis"
    load_dotenv(env_path)
    
    OPENAI_API = os.getenv("OPENAI_API_KEY")
    print(OPENAI_API)
