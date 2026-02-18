from src.data.models.models import *

from src.app.responses.response import *


class Mapper:
    def map_user(self, user_model: UserModel) -> UserResponse:
        return UserResponse(
            email=user_model.email,
            first_name=user_model.first_name,
            last_name=user_model.last_name,
        )

    def map_blog(self, blog_model: BlogModel) -> BlogResponse:
        return BlogResponse(
            id=blog_model.id,
            title=blog_model.title,
            content=blog_model.content,
        )
