from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from app.settings import get_settings

settings = get_settings()

model = ChatGoogleGenerativeAI(model=settings.model_name,
                               max_output_tokens=settings.max_output_tokens,
                               api_key=settings.google_api_key)
agent = create_agent(model)


async def pipeline(input_text: str):
    messages = {"messages": [{"role": "user", "content": input_text}]}
    result = await agent.ainvoke(messages)
    return result
