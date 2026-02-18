import logging
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.client import MultiServerMCPClient

from app.schemas.schemas import AgentResponse
from app.settings import get_settings

logger = logging.getLogger("uvicorn.error")

settings = get_settings()

system_prompt = """
You are Chef in My Pocket, an AI meal-planning agent.

Your role is to help users create a multi-day meal plan based on a dietary goal and automatically generate a consolidated shopping list using available tools.
You have access to the following tools:

recipe_finder()
→ Returns a list of all available recipe names.

get_ingridients(recipe: str)
→ Returns a list of ingredients for a specific recipe.

You MUST use tools when recipe or ingredient information is required.
You MUST NOT hallucinate recipe names or ingredients.
User sends you number of days for the meal plan cover.
ASSUME 1 MAIN MEAL PER DAY UNLESS USER SPECIFIES OTHERWISE

Your final response must contain:
Meal plan
Shopping List
"""

model = ChatGoogleGenerativeAI(
    model=settings.model_name,
    max_output_tokens=settings.max_output_tokens,
    api_key=settings.google_api_key,
)


class Agent:
    async def setup(self):
        client = MultiServerMCPClient(
            {"chef_mcp": {"transport": "http", "url": str(settings.mcp_url)}}
        )
        tools = await client.get_tools()
        self.agent = create_agent(model, tools=tools, system_prompt=system_prompt)

        logger.info("Agent is ready")

    async def pipeline(self, input_text: str):
        messages = {"messages": [{"role": "user", "content": input_text}]}
        # config: RunnableConfig = {"configurable": {"thread_id": "1"}}
        result = await self.agent.ainvoke(messages)
        messages = result["messages"]
        last_ai = next(
            m for m in reversed(messages) if getattr(m, "type", None) == "ai"
        )
        final_text = last_ai.text
        return AgentResponse(content=final_text)
