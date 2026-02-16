from src.app.responses.response import *
from src.data.models.models import *


class ReverseMapper:
    def r_map_user(self, user_response: UserResponse, encrypted_password: str) -> UserModel:
        return UserModel(
            email=user_response.email,
            first_name=user_response.first_name,
            last_name=user_response.last_name,
            encrypted_password=encrypted_password,
        )

    def r_map_blog(self, blog_response: BlogResponse) -> BlogModel:
        return BlogModel(
            title=blog_response.title,
            content=blog_response.content,
        )
