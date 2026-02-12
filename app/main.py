import logging
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse

from app.settings import Settings, get_settings
from app.agent import Agent

logger = logging.getLogger("uvicorn.error")


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


@app.post("/chat")
async def chat(input_data, settings: Annotated[Settings, Depends(get_settings)]):
    try:
        logger.info(f"Question {settings.model_name}: '{input_data}'")
        response = await app.state.agent.pipeline(input_data)
        logger.info(f"Response: '{response}'")
        return response
    except Exception as e:
        logger.exception("API Exception")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
