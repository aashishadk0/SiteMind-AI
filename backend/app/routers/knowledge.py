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
            name=request.name,
            url=request.url,
            max_pages=request.max_pages
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@router.get("/sources")
def sources():
    return service.list_sources()


@router.delete("/sources/{source_id}")
def delete_source(source_id: int):
    return service.delete_source(source_id)