from typing import Optional

from pydantic import BaseModel


class RegisterRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str


class CreateBlogRequest(BaseModel):
    title: str
    content: str


class UpdateBlogRequest(BaseModel):
    new_title: Optional[str]
    new_content: Optional[str]


class UpdateUserRequest(BaseModel):
    new_first_name: Optional[str]
    new_last_name: Optional[str]
