from typing import Optional
from pydantic import BaseModel, Field, model_validator

from src.app.validators.validators import Validators


class BaseModelRequest(BaseModel):
    model_config = {
        "str_strip_whitespace": True,
    }


class RegisterRequest(BaseModelRequest):
    first_name: str = Field(min_length=2, max_length=50)
    last_name: str = Field(min_length=2, max_length=50)
    email: str = Field(min_length=6, max_length=50)
    password: str = Field(min_length=8, max_length=128)

    @model_validator(mode="after")
    def validate_fields(self):
        Validators.validate_email(self.email)
        Validators.validate_password(self.password)
        return self


class CreateBlogRequest(BaseModelRequest):
    title: str = Field(min_length=3, max_length=150)
    content: str = Field(min_length=10, max_length=5000)


class UpdateBlogRequest(BaseModelRequest):
    new_title: Optional[str] = Field(default=None, min_length=3, max_length=150)
    new_content: Optional[str] = Field(default=None, min_length=10, max_length=5000)

    @model_validator(mode="after")
    def validate_fields(self):
        Validators.at_least_one_valid([self.new_title, self.new_content])
        return self


class UpdateUserRequest(BaseModelRequest):
    new_first_name: Optional[str] = Field(default=None, min_length=2, max_length=50)
    new_last_name: Optional[str] = Field(default=None, min_length=2, max_length=50)

    @model_validator(mode="after")
    def validate_fields(self):
        Validators.at_least_one_valid([self.new_first_name, self.new_last_name])
        return self
