import sqlalchemy
from sqlalchemy.orm import relationship

import src.infrastructure.alchemy_sql as alchemy_sql


class UserModel(alchemy_sql.Base):
    __tablename__ = "users"

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        unique=True,
        autoincrement=True,
        index=True
    )

    email = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False,
        unique=True,
    )

    first_name = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False,
    )

    last_name = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False,
    )

    encrypted_password = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False,
    )

    # ONE user → MANY blogs
    blogs = relationship(
        "BlogModel",
        back_populates="creator",
        cascade="all, delete-orphan"
    )


class BlogModel(alchemy_sql.Base):
    __tablename__ = "blogs"

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        unique=True,
        autoincrement=True,
        index=True
    )

    title = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False,
    )

    content = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False,
    )

    # Foreign key to user
    creator_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("users.id"),
        nullable=False,
    )

    # RELATION back to user
    creator = relationship(
        "UserModel",
        back_populates="blogs"
    )
