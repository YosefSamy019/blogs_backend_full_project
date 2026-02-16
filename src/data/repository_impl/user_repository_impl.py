from src.app.requests.requests import UpdateUserRequest
from src.app.responses.response import *
from src.data.datasources.cache_data_source import CacheDataSource
from src.data.failure import Failure
from src.data.models.models import UserModel
from src.data.services.hash_service import HashService
from src.data.services.jwt_service import JWTService
from src.domain.mappers.mappers import Mapper
from src.domain.mappers.reverse_mappers import ReverseMapper
from src.domain.repository.user_repository import UserRepository
from src.shared.either import Either, left, right
from src.shared.env import Env


class UserRepositoryImpl(UserRepository):

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

    def get_user_data(self, jwt_token: str) -> Either[Failure, UserResponse]:
        try:
            email: str | None = self.jwt_service.verify_login_token(jwt_token)
            if email is None:
                return left(Failure.wrong_access_token())
            else:
                user_model: UserModel = self.cache_data_source.get_user_by_email(email)
                user_response: UserResponse = self.mapper.map_user(user_model)
                return right(user_response)

        except Exception as e:
            failure = Failure.handle_error(e)
            return left(failure)

    def update_user_data(self, jwt_token: str, request: UpdateUserRequest) -> Either[Failure, UserResponse]:
        try:
            email: str | None = self.jwt_service.verify_login_token(jwt_token)
            assert email is not None, Failure.wrong_access_token()

            user_model: UserModel = self.cache_data_source.get_user_by_email(email)

            self.cache_data_source.update_existing_user(
                user_id=user_model.id,
                first_name=request.new_first_name,
                last_name=request.new_last_name,
            )

            user_model: UserModel = self.cache_data_source.get_user_by_email(email)
            user_response: UserResponse = self.mapper.map_user(user_model)

            return right(user_response)

        except Exception as e:
            failure = Failure.handle_error(e)
            return left(failure)
