from abc import ABC, abstractmethod

from src.app.requests.requests import *
from src.app.responses.response import UserResponse
from src.data.failure import Failure
from src.shared.either import Either


class UserRepository(ABC):
    @abstractmethod
    def get_user_data(self, jwt_token: str) -> Either[Failure, UserResponse]:
        raise NotImplementedError

    @abstractmethod
    def update_user_data(self, jwt_token: str, request: UpdateUserRequest) ->  Either[Failure, UserResponse]:
        raise NotImplementedError
