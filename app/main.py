import logging
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse

from app.settings import Settings, get_settings
from app.agent import Agent
from app.schemas.schemas import UserQuestion, AgentResponse

logger = logging.getLogger("uvicorn.error")

# DB_URI = "postgresql://postgres:postgres@localhost:5432/postgres?sslmode=disable"

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
#         checkpointer.setup()
#         agent = Agent()
#         await agent.setup(checkpointer)
#         app.state.agent = agent
#         logger.info("Application startup complete")
#         yield
#         logger.info("Application shutdown")


@asynccontextmanager
async def lifespan(app: FastAPI):
    agent = Agent()
    await agent.setup()
    app.state.agent = agent
    logger.info("Application startup complete")
    yield
    logger.info("Application shutdown")


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return RedirectResponse("/docs")


@app.post("/chat", response_model=AgentResponse)
async def chat(
    input_data: UserQuestion, settings: Annotated[Settings, Depends(get_settings)]
):
    try:
        logger.info(f"Question {settings.model_name}: '{input_data.content}'")
        response = await app.state.agent.pipeline(input_data.content)
        logger.info(f"Response: '{response}'")
        return response
    except Exception as e:
        logger.exception("API Exception")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
