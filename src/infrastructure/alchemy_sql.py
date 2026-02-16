from typing import Generator
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from src.shared.env import Env

# -------------------------
# SQLAlchemy setup
# -------------------------
engine = create_engine(
    Env().sql_alchemy_db_url(),
    connect_args={"check_same_thread": False},  # for SQLite
    echo=Env().is_debug(),
)

curSessionMaker = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# -------------------------
# DB Provider with context manager
# -------------------------
class DBProvider:
    def __init__(self):
        pass  # required because __init__ cannot be empty

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """Provide a transactional scope around a series of operations."""
        db: Session = curSessionMaker()  # create session
        try:
            yield db  # provide session to `with` block
        finally:
            db.close()  # automatically close after block
