from abc import ABC, abstractmethod

from src.app.requests.requests import *
from src.app.responses.response import *
from src.data.failure import Failure
from src.shared.either import Either


class BlogRepository(ABC):
    @abstractmethod
    def get_blog(self, jwt_token: str, blog_id: int) -> Either[Failure, BlogResponse]:
        raise NotImplementedError

    @abstractmethod
    def get_blogs_page(self, jwt_token: str, page_index: int) -> Either[Failure, BlogPageResponse]:
        raise NotImplementedError

    @abstractmethod
    def create_blog(self, jwt_token: str, request: CreateBlogRequest) -> Either[Failure, BlogResponse]:
        raise NotImplementedError

    @abstractmethod
    def update_blog(self, jwt_token: str, request: UpdateBlogRequest, blog_id: int) -> Either[Failure, BlogResponse]:
        raise NotImplementedError

    @abstractmethod
    def delete_blog(self, jwt_token: str, blog_id: int) -> Either[
        Failure, DeleteBlogResponse]:
        raise NotImplementedError
