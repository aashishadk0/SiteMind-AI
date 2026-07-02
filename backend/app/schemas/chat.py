from pydantic import BaseModel


class ChatRequest(BaseModel):

    chat_id: int

    question: str

    provider: str

    model: str


class ChatResponse(BaseModel):

    answer: str

    sources: list