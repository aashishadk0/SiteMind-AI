"""
Knowledge source API.
"""

from fastapi import APIRouter, HTTPException

from backend.app.schemas.knowledge import IndexWebsiteRequest
from backend.app.services.knowledge_service import KnowledgeService


router = APIRouter(
    prefix="/knowledge",
    tags=["Knowledge"]
)

service = KnowledgeService()


@router.post("/index")
def index_website(request: IndexWebsiteRequest):
    try:
        return service.index_website(
            user_id=request.user_id,
            name=request.name,
            url=request.url,
            max_pages=request.max_pages
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@router.get("/sources/{user_id}")
def sources(user_id: int):
    return service.list_sources(user_id)


@router.get("/sources/{user_id}/{source_id}")
def source_detail(user_id: int, source_id: int):
    source = service.get_source(source_id, user_id)

    if not source:
        raise HTTPException(
            status_code=404,
            detail="Knowledge source not found."
        )

    return source


@router.delete("/sources/{user_id}/{source_id}")
def delete_source(user_id: int, source_id: int):
    return service.delete_source(source_id, user_id)