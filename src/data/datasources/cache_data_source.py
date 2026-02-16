from abc import ABC, abstractmethod
from typing import List, Optional

from src.data.models.models import *


class CacheDataSource(ABC):
    @abstractmethod
    def get_user(self, user_id: int) -> UserModel:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> UserModel:
        pass

    @abstractmethod
    def create_new_user(self, user: UserModel) -> UserModel:
        pass

    @abstractmethod
    def update_existing_user(self,
                             first_name: Optional[str],
                             last_name: Optional[str],
                             user_id: int) -> None:
        pass

    @abstractmethod
    def get_blogs_page(self, user_id: int, start_index: int, page_size: int) -> List[BlogModel]:
        pass

    @abstractmethod
    def count_blogs(self, user_id: int) -> int:
        pass

    @abstractmethod
    def get_blog(self, user_id: int, blog_id: int) -> BlogModel:
        pass

    @abstractmethod
    def create_new_blog(self, blog: BlogModel) -> BlogModel:
        pass

    @abstractmethod
    def update_existing_blog(self,
                             blog_title: str,
                             blog_content: str,
                             blog_id: int) -> None:
        pass

    @abstractmethod
    def delete_existing_blog(self, blog_id: int) -> None:
        pass
