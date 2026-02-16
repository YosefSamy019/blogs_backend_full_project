from typing import Generic, TypeVar, Union
from dataclasses import dataclass

L = TypeVar("L")  # Left type (Error)
R = TypeVar("R")  # Right type (Success)


@dataclass
class Left(Generic[L, R]):
    value: L


@dataclass
class Right(Generic[L, R]):
    value: R


Either = Union[Left[L, R], Right[L, R]]


# Helper functions
def left(value: L) -> Either[L, R]:
    return Left(value)


def right(value: R) -> Either[L, R]:
    return Right(value)
