from pydantic import BaseModel


class IndexWebsiteRequest(BaseModel):
    name: str
    url: str
    max_pages: int = 20