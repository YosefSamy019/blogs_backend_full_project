from src.data.datasources.cache_data_source import CacheDataSource
from src.data.datasources.cache_data_source_alchemy_impl import CacheDataSourceAlChemyImpl
from src.data.repository_impl.auth_repository_impl import AuthRepositoryImpl
from src.data.repository_impl.blog_repository_impl import BlogRepositoryImpl
from src.data.repository_impl.user_repository_impl import UserRepositoryImpl
from src.data.services.hash_service import HashService
from src.data.services.jwt_service import JWTService
from src.domain.mappers.mappers import Mapper
from src.domain.mappers.reverse_mappers import ReverseMapper
from src.domain.repository.auth_repository import AuthRepository
from src.domain.repository.blog_repository import BlogRepository
from src.domain.repository.user_repository import UserRepository
from src.infrastructure.alchemy_sql import Base, engine, DBProvider
from src.shared.env import Env


class Sl:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Sl, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return  # Already initialized

        self.env: Env = Env()

        # --- Initialization ---
        self.alchemy_db_provider = DBProvider()
        Base.metadata.create_all(bind=engine)

        self.cache_data_source: CacheDataSource = CacheDataSourceAlChemyImpl(
            alchemy_db_provider=self.alchemy_db_provider
        )

        self.mapper: Mapper = Mapper()
        self.reverse_mapper: ReverseMapper = ReverseMapper()

        self.hash_services: HashService = HashService()
        self.jwt_service: JWTService = JWTService(
            secret_key=self.env.secret_key(),
            algorithm=self.env.algorithm(),
        )

        self.auth_repository: AuthRepository = AuthRepositoryImpl(
            cache_data_source=self.cache_data_source,
            mapper=self.mapper,
            reverse_mapper=self.reverse_mapper,
            hash_service=self.hash_services,
            jwt_service=self.jwt_service,
            env=self.env,
        )

        self.blog_repository: BlogRepository = BlogRepositoryImpl(
            cache_data_source=self.cache_data_source,
            mapper=self.mapper,
            reverse_mapper=self.reverse_mapper,
            hash_service=self.hash_services,
            jwt_service=self.jwt_service,
            env=self.env,
        )

        self.user_repository: UserRepository = UserRepositoryImpl(
            cache_data_source=self.cache_data_source,
            mapper=self.mapper,
            reverse_mapper=self.reverse_mapper,
            hash_service=self.hash_services,
            jwt_service=self.jwt_service,
            env=self.env,
        )

        self._initialized = True  # Mark as initialized
