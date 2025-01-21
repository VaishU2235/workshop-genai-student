from langchain_anthropic import ChatAnthropic
import os

def get_llm_model():
    # Initialize Claude model with environment variable
    claude = ChatAnthropic(
        anthropic_api_key=os.getenv('ANTHROPIC_API_KEY'),
        model="claude-3-sonnet-20240229",
        temperature=0.7
    )
    return claude