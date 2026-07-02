from fastapi import APIRouter

router = APIRouter(
    prefix="/scraper",
    tags=["Scraper"]
)


@router.get("/test")
def test():

    return {
        "message": "Scraper API Working"
    }