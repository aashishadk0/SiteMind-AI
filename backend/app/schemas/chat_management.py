from pydantic import BaseModel


class CreateChatRequest(BaseModel):

    user_id: int


class RenameChatRequest(BaseModel):

    title: str