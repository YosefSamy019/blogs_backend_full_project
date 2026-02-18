from fastapi import APIRouter, Depends, status

import src.app.requests.requests as requests
from src.app.responses.response import UserResponse
from src.app.routes.oauth import get_access_token
from src.shared.either import Either, Right
from src.shared.sl import Sl

users_router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"],
)


@users_router.get("/me",
                  response_model=UserResponse,
                  status_code=status.HTTP_200_OK)
async def get_me(
        access_token: str = Depends(get_access_token),
):
    ret_val: Either = Sl().user_repository.get_user_data(access_token)
    return Sl().response_process.process(ret_val)


@users_router.put("/me",
                  response_model=UserResponse,
                  status_code=status.HTTP_200_OK)
async def update_me(
        request: requests.UpdateUserRequest,
        access_token: str = Depends(get_access_token),
):
    ret_val: Either = Sl().user_repository.update_user_data(
        jwt_token=access_token,
        request=request,
    )

    return Sl().response_process.process(ret_val)
