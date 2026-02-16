import math
from typing import List

from src.app.requests.requests import UpdateBlogRequest, CreateBlogRequest
from src.app.responses.response import DeleteBlogResponse, BlogResponse, BlogPageResponse
from src.data.datasources.cache_data_source import CacheDataSource
from src.data.failure import Failure
from src.data.models.models import *
from src.data.services.hash_service import HashService
from src.data.services.jwt_service import JWTService
from src.domain.mappers.mappers import Mapper
from src.domain.mappers.reverse_mappers import ReverseMapper
from src.domain.repository.blog_repository import BlogRepository
from src.shared.either import Either, left, right
from src.shared.env import Env


class BlogRepositoryImpl(BlogRepository):

    def __init__(self,
                 cache_data_source: CacheDataSource,
                 mapper: Mapper,
                 reverse_mapper: ReverseMapper,
                 hash_service: HashService,
                 jwt_service: JWTService,
                 env: Env
                 ) -> None:
        self.cache_data_source = cache_data_source
        self.mapper = mapper
        self.reverse_mapper = reverse_mapper
        self.hash_service = hash_service
        self.jwt_service = jwt_service
        self.env = env

    def get_blog(self, jwt_token: str, blog_id: int) -> Either[Failure, BlogResponse]:
        try:
            email: str | None = self.jwt_service.verify_login_token(jwt_token)

            if email is None:
                return left(Failure.wrong_access_token())
            else:
                user_model: UserModel = self.cache_data_source.get_user_by_email(email)

                blog_model: BlogModel = self.cache_data_source.get_blog(
                    user_id=user_model.id,
                    blog_id=blog_id
                )

                blog_response: BlogResponse = self.mapper.map_blog(blog_model)

                return right(blog_response)

        except Exception as e:
            failure = Failure.handle_error(e)
            return left(failure)

    def get_blogs_page(self, jwt_token: str, page_index: int) -> Either[Failure, BlogPageResponse]:
        try:
            email: str | None = self.jwt_service.verify_login_token(jwt_token)

            if email is None:
                return left(Failure.wrong_access_token())
            else:
                user_model: UserModel = self.cache_data_source.get_user_by_email(email)
                n_blogs = self.cache_data_source.count_blogs(user_id=user_model.id)
                n_pages = math.ceil(n_blogs / self.env.page_size())

                blogs_models_list: List[BlogModel] = self.cache_data_source.get_blogs_page(
                    user_id=user_model.id,
                    page_size=self.env.page_size(),
                    start_index=page_index * self.env.page_size()
                )

                blogs_responses_list = list(map(lambda blog: self.mapper.map_blog(blog), blogs_models_list))

                return right(BlogPageResponse(
                    page_size=self.env.page_size(),
                    blogs=blogs_responses_list,
                    total_pages=n_pages
                ))

        except Exception as e:
            failure = Failure.handle_error(e)
            return left(failure)

    def create_blog(self, jwt_token: str, request: CreateBlogRequest) -> Either[Failure, BlogResponse]:
        try:
            email: str | None = self.jwt_service.verify_login_token(jwt_token)

            if email is None:
                return left(Failure.wrong_access_token())
            else:
                user_model: UserModel = self.cache_data_source.get_user_by_email(email)

                blog_model: BlogModel = BlogModel(
                    title=request.title,
                    content=request.content,
                    creator_id=user_model.id,
                )

                blog_model: BlogModel = self.cache_data_source.create_new_blog(
                    blog=blog_model,
                )

                blog_response: BlogResponse = self.mapper.map_blog(blog_model)

                return right(blog_response)

        except Exception as e:
            failure = Failure.handle_error(e)
            return left(failure)

    def update_blog(self, jwt_token: str, request: UpdateBlogRequest, blog_id: int) -> Either[Failure, BlogResponse]:
        try:
            email: str | None = self.jwt_service.verify_login_token(jwt_token)

            if email is None:
                return left(Failure.wrong_access_token())
            else:
                user_model: UserModel = self.cache_data_source.get_user_by_email(email)

                blog_model: BlogModel = self.cache_data_source.get_blog(
                    user_id=user_model.id,
                    blog_id=blog_id
                )

                self.cache_data_source.update_existing_blog(
                    blog_id=blog_id,
                    blog_title=request.new_title,
                    blog_content=request.new_content,
                )

                blog_model: BlogModel = self.cache_data_source.get_blog(
                    user_id=user_model.id,
                    blog_id=blog_id
                )

                blog_response: BlogResponse = self.mapper.map_blog(blog_model)

                return right(blog_response)

        except Exception as e:
            failure = Failure.handle_error(e)
        return left(failure)

    def delete_blog(self, jwt_token: str,
                    blog_id: int) -> Either[
        Failure, DeleteBlogResponse]:
        try:
            email: str | None = self.jwt_service.verify_login_token(jwt_token)

            if email is None:
                return left(Failure.wrong_access_token())
            else:
                user_model: UserModel = self.cache_data_source.get_user_by_email(email)

                blog_model: BlogModel = self.cache_data_source.get_blog(
                    user_id=user_model.id,
                    blog_id=blog_id
                )

                self.cache_data_source.delete_existing_blog(
                    blog_id=blog_id,
                )

                return right(DeleteBlogResponse(id=blog_id))

        except Exception as e:
            failure = Failure.handle_error(e)
        return left(failure)
