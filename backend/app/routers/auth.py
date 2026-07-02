from fastapi import APIRouter, HTTPException

from backend.app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    AuthResponse
)

from backend.app.services.auth_service import AuthService


router = APIRouter(

    prefix="/auth",

    tags=["Authentication"]

)

service = AuthService()


@router.post(

    "/register",

    response_model=AuthResponse

)
def register(
    request: RegisterRequest
):

    try:

        return service.register(

            request.username,

            request.email,

            request.password

        )

    except Exception as e:

        raise HTTPException(

            status_code=400,

            detail=str(e)

        )


@router.post(

    "/login",

    response_model=AuthResponse

)
def login(
    request: LoginRequest
):

    try:

        return service.login(

            request.email,

            request.password

        )

    except Exception as e:

        raise HTTPException(

            status_code=401,

            detail=str(e)

        )