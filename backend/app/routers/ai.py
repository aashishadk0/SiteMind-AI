from fastapi import APIRouter, HTTPException

from backend.app.core.model_manager import ModelManager

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)



@router.get("/models")
def get_models():

    return ModelManager.get_all()


@router.get("/providers")
def providers():

    return list(
        ModelManager.get_all().keys()
    )


@router.get("/default/{provider}")
def default_model(provider: str):

    provider = provider.lower()

    if not ModelManager.get_provider(provider):

        raise HTTPException(
            status_code=404,
            detail=f"Provider '{provider}' not found."
        )

    return {
        "provider": provider,
        "default_model": ModelManager.default_model(provider)
    }