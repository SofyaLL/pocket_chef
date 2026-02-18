from pydantic import BaseModel, Field


class UserQuestion(BaseModel):
    content: str = Field(
        min_length=5, max_length=240, description="User input to agent"
    )


class AgentResponse(BaseModel):
    content: str
