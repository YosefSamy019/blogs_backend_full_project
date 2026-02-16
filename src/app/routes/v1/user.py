from fastapi import APIRouter, Depends, status

import src.app.requests.requests as requests
from src.app.routes.oauth import get_access_token
from src.shared.either import Either, Right
from src.shared.sl import Sl

users_router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"],
)


@users_router.get("/me", status_code=status.HTTP_200_OK)
async def get_me(
        access_token: str = Depends(get_access_token),
):
    ret_val: Either = Sl().user_repository.get_user_data(access_token)
    if isinstance(ret_val, Right):
        return ret_val.value
    else:
        return ret_val.__dict__


@users_router.put("/me", status_code=status.HTTP_202_ACCEPTED)
async def update_me(
        request: requests.UpdateUserRequest,
        access_token: str = Depends(get_access_token),
):
    ret_val: Either = Sl().user_repository.update_user_data(
        jwt_token=access_token,
        request=request,
    )

    if isinstance(ret_val, Right):
        return ret_val.value
    else:
        return ret_val.__dict__
