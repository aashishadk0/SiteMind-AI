from pydantic import BaseModel


class IndexWebsiteRequest(BaseModel):
    user_id: int
    name: str
    url: str
    max_pages: int = 40


class ListSourcesRequest(BaseModel):
    user_id: int