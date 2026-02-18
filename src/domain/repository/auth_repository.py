from abc import ABC, abstractmethod

from src.shared.either import Either

from src.data.failure import Failure

from src.app.requests.requests import *
from src.app.responses.response import *


class AuthRepository(ABC):
    @abstractmethod
    def register(self, request: RegisterRequest) -> Either[Failure, UserResponse]:
        raise NotImplementedError

    @abstractmethod
    def login(self, email: str, password: str) -> Either[Failure, LoginResponse]:
        raise NotImplementedError
