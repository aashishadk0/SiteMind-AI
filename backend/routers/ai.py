from fastapi import APIRouter

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


@router.get("/test")
def test():

    return {
        "message": "AI API Working"
    }