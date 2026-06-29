from fastapi import APIRouter

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.get("/test")
def test():

    return {
        "message": "Chat API Working"
    }