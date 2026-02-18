from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from src.app.requests.requests import *
from src.app.responses.response import LoginResponse, UserResponse
from src.shared.either import Either, Right
from src.shared.sl import Sl

auth_router = APIRouter(
    tags=["auth"],
    prefix="/api/v1/auth",
)


@auth_router.post("/register",
                  response_model=UserResponse,
                  status_code=status.HTTP_201_CREATED)
async def register_user(
        request: RegisterRequest,
):
    ret_val: Either = Sl().auth_repository.register(request)
    return Sl().response_process.process(ret_val)


@auth_router.post("/login",
                  response_model=LoginResponse,
                  status_code=status.HTTP_200_OK)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
):
    user_email = form_data.username
    user_pwd = form_data.password

    ret_val: Either = Sl().auth_repository.login(email=user_email, password=user_pwd)
    return Sl().response_process.process(ret_val)
