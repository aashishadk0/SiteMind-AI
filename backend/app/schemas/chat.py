from pydantic import BaseModel


class ChatRequest(BaseModel):
    chat_id: int
    user_id: int
    source_id: int | None = None
    question: str
    provider: str
    model: str


class ChatResponse(BaseModel):
    answer: str
    sources: list