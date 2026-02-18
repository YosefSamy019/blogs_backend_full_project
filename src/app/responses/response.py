from typing import Optional, List

from pydantic import BaseModel, Field


class BaseResponseModel(BaseModel):
    pass


class BlogResponse(BaseResponseModel):
    id: int
    title: str
    content: str


class BlogPageResponse(BaseResponseModel):
    page_size: int
    blogs: List[BlogResponse]
    total_pages: int


class DeleteBlogResponse(BaseResponseModel):
    id: int


class UserResponse(BaseResponseModel):
    first_name: str
    last_name: str
    email: str


class LoginResponse(BaseResponseModel):
    access_token: str
    token_type: str
    user: UserResponse
