from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import get_user_service
from app.exceptions.base import (
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    UnknownUserCreateError,
    UsernameAlreadyExistsError,
)
from app.features.users.schemas import (
    TokenResponse,
    UserCreate,
    UserLogin,
    UserResponse,
)
from app.features.users.services import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", response_model=UserResponse, summary="Sign UP")
async def create_user_endpoint(data: UserCreate, service: Annotated[UserService, Depends(get_user_service)]):
    try:
        return await service.create_user(data)

    except EmailAlreadyExistsError:
        raise HTTPException(
            status_code=409,
            detail="User with this email already exists",
        )

    except UsernameAlreadyExistsError:
        raise HTTPException(
            status_code=409,
            detail="User with this username already exists",
        )

    except UnknownUserCreateError:
        raise HTTPException(
            status_code=404,
            detail="Unknown user error"
        )


@router.post("/auth", response_model=TokenResponse, summary="Sign IN")
async def login_user_endpoint(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                              service: Annotated[UserService, Depends(get_user_service)]):
    try:
        user_login = UserLogin(username=form_data.username, password=form_data.password)
        return await service.login_user(user_login)

    except InvalidCredentialsError:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )