from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from src.app.requests.requests import RegisterRequest
from src.shared.either import Either, Right
from src.shared.sl import Sl

auth_router = APIRouter(
    tags=["auth"],
    prefix="/api/v1/auth",
)


@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
        request: RegisterRequest,
):
    ret_val: Either = Sl().auth_repository.register(request)
    if isinstance(ret_val, Right):
        return ret_val.value
    else:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(ret_val.__dict__))


@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
):
    user_email = form_data.username
    user_pwd = form_data.password

    ret_val: Either = Sl().auth_repository.login(email=user_email, password=user_pwd)
    if isinstance(ret_val, Right):
        return ret_val.value
    else:
        return ret_val.__dict__
