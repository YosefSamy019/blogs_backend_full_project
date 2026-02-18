from typing import List, Optional
from sqlalchemy.orm import Session
from src.infrastructure.alchemy_sql import DBProvider

from src.data.datasources.cache_data_source import CacheDataSource
from src.data.models.models import *
from src.data.failure import Failure


class CacheDataSourceAlChemyImpl(CacheDataSource):

    def __init__(self, alchemy_db_provider: DBProvider):
        self._db_provider: DBProvider = alchemy_db_provider

    def get_user(self, user_id: int) -> UserModel:
        with self._db_provider.get_session() as _db:
            val = _db.query(UserModel).filter(
                UserModel.id == user_id
            ).first()

            if val is None:
                raise Failure.user_not_found(user_id=user_id)
            else:
                return val

    def get_user_by_email(self, email: str) -> UserModel:
        with self._db_provider.get_session() as _db:
            val = _db.query(UserModel).filter(
                UserModel.email == email
            ).first()

            if val is None:
                raise Failure.user_not_found_with_email(email=email)
            else:
                return val

    def create_new_user(self, user: UserModel) -> UserModel:
        with self._db_provider.get_session() as _db:
            _db.add(user)
            _db.commit()
            _db.refresh(user)
            return user

    def update_existing_user(self,
                             first_name: Optional[str],
                             last_name: Optional[str],
                             user_id: int) -> None:
        with self._db_provider.get_session() as _db:
            update_dict = dict()
            if first_name is not None:
                update_dict[f"{UserModel.first_name.name}"] = first_name
            if last_name is not None:
                update_dict[f"{UserModel.last_name.name}"] = last_name

            if len(update_dict) > 0:
                val: int = _db.query(UserModel).filter(
                    UserModel.id == user_id
                ).update(update_dict)

                _db.commit()

                if val == 0:
                    raise Failure.user_not_found(user_id=user_id)

    def get_blogs_page(self, user_id: int, start_index: int, page_size: int) -> List[BlogModel]:
        with self._db_provider.get_session() as _db:
            values: list = _db.query(BlogModel).filter(
                BlogModel.creator_id == user_id
            ).offset(start_index).limit(page_size).all()

            return values

    def count_blogs(self, user_id: int) -> int:
        with self._db_provider.get_session() as _db:
            value: int = _db.query(BlogModel).filter(
                BlogModel.creator_id == user_id
            ).count()

            return value

    def create_new_blog(self, blog: BlogModel) -> BlogModel:
        with self._db_provider.get_session() as _db:
            _db.add(blog)
            _db.commit()
            _db.refresh(blog)
            return blog

    def update_existing_blog(self,
                             blog_title: str,
                             blog_content: str,
                             blog_id: int) -> None:
        with self._db_provider.get_session() as _db:
            update_dict = dict()

            if blog_title is not None:
                update_dict[f"{BlogModel.title.name}"] = blog_title
            if blog_content is not None:
                update_dict[f"{BlogModel.content.name}"] = blog_content

            if len(update_dict) > 0:
                val: int = _db.query(BlogModel).filter(
                    BlogModel.id == blog_id
                ).update(update_dict)

                _db.commit()

                if val == 0:
                    raise Failure.blog_not_found(blog_id=blog_id)

    def delete_existing_blog(self, blog_id: int) -> None:
        with self._db_provider.get_session() as _db:
            val: int = _db.query(BlogModel).filter(
                BlogModel.id == blog_id
            ).delete(
                synchronize_session=False
            )
            _db.commit()

            if val == 0:
                # Blog Not fount
                raise Failure.blog_not_found(blog_id=blog_id)

    def get_blog(self, user_id: int, blog_id: int) -> BlogModel:
        with self._db_provider.get_session() as _db:
            val: BlogModel = _db.query(BlogModel).filter(
                BlogModel.id == blog_id,
                BlogModel.creator_id == user_id
            ).first()

            if val is None:
                raise Failure.blog_not_found(blog_id=blog_id)
            else:
                return val
