from typing import Optional, List

from pydantic import BaseModel, Field


class BlogResponse(BaseModel):
    id: int
    title: str
    content: str


class BlogPageResponse(BaseModel):
    page_size:int
    blogs: List[BlogResponse]
    total_pages: int


class DeleteBlogResponse(BaseModel):
    id: int


class UserResponse(BaseModel):
    first_name: str
    last_name: str
    email: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse
