from src.app.requests.requests import *
from src.app.responses.response import *
from src.data.datasources.cache_data_source import CacheDataSource
from src.data.failure import Failure
from src.data.models.models import UserModel
from src.data.services.jwt_service import JWTService
from src.domain.mappers.mappers import Mapper
from src.domain.mappers.reverse_mappers import ReverseMapper
from src.domain.repository.auth_repository import AuthRepository
import src.data.models.models as models
from src.data.services.hash_service import HashService
from src.shared.either import Either, right, left
from src.shared.env import Env


class AuthRepositoryImpl(AuthRepository):

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

    def register(self, request: RegisterRequest) -> Either[Failure, UserResponse]:
        try:

            try:
                self.cache_data_source.get_user_by_email(request.email)
                return left(Failure.duplicated_email(request.email))
            except Exception as e:
                # Email not fount in DB
                pass

            encrypted_pwd = self.hash_service.hash(request.password)

            new_user: models.UserModel = models.UserModel(
                email=request.email,
                last_name=request.last_name,
                first_name=request.first_name,
                encrypted_password=encrypted_pwd,
            )

            new_user_model: UserModel = self.cache_data_source.create_new_user(
                user=new_user,
            )

            new_user_response: UserResponse = self.mapper.map_user(new_user_model)
            return right(new_user_response)

        except Exception as e:
            failure = Failure.handle_error(e)
            return left(failure)

    def login(self, email: str, password: str) -> Either[Failure, LoginResponse]:

        try:
            user_model: UserModel = self.cache_data_source.get_user_by_email(email)

            user_verified: bool = self.hash_service.verify(password, user_model.encrypted_password)

            if not user_verified:
                return left(Failure.wrong_password())

            else:
                jwt_token = self.jwt_service.generate_login_token(email=email)

                user_response = self.mapper.map_user(user_model)

                login_response: LoginResponse = LoginResponse(
                    user=user_response,
                    access_token=jwt_token,
                    token_type="Bearer",
                )

                return right(login_response)

        except Exception as e:
            # No User found with email
            failure = Failure.handle_error(e)
            return left(failure)
