from fastapi import APIRouter, Depends, status
import src.app.requests.requests as requests
from src.app.routes.oauth import get_access_token
from src.shared.either import Either, Right
from src.shared.sl import Sl

blogs_router = APIRouter(
    prefix="/api/v1/blogs",
    tags=["blogs"],
)


@blogs_router.get("/{blog_id}", status_code=status.HTTP_200_OK)
async def get_blog(
        blog_id: int,
        access_token: str = Depends(get_access_token),
):
    ret_val: Either = Sl().blog_repository.get_blog(
        blog_id=blog_id,
        jwt_token=access_token,
    )

    if isinstance(ret_val, Right):
        return ret_val.value
    else:
        return ret_val.__dict__


@blogs_router.get("/page/{page_index}", status_code=status.HTTP_200_OK)
async def get_blogs(
        page_index: int,
        access_token: str = Depends(get_access_token),
):
    ret_val: Either = Sl().blog_repository.get_blogs_page(
        page_index=page_index,
        jwt_token=access_token,
    )

    if isinstance(ret_val, Right):
        return ret_val.value
    else:
        return ret_val.__dict__


@blogs_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_blog(
        request: requests.CreateBlogRequest,
        access_token: str = Depends(get_access_token),
):
    ret_val: Either = Sl().blog_repository.create_blog(
        request=request,
        jwt_token=access_token,
    )

    if isinstance(ret_val, Right):
        return ret_val.value
    else:
        return ret_val.__dict__


@blogs_router.put("/{blog_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_blog(
        blog_id: int,
        request: requests.UpdateBlogRequest,
        access_token: str = Depends(get_access_token),
):
    ret_val: Either = Sl().blog_repository.update_blog(
        request=request,
        jwt_token=access_token,
        blog_id=blog_id,
    )

    if isinstance(ret_val, Right):
        return ret_val.value
    else:
        return ret_val.__dict__


@blogs_router.delete("/{blog_id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_blog(
        blog_id: int,
        access_token: str = Depends(get_access_token),
):
    ret_val: Either = Sl().blog_repository.delete_blog(
        jwt_token=access_token,
        blog_id=blog_id,
    )

    if isinstance(ret_val, Right):
        return ret_val.value
    else:
        return ret_val.__dict__
