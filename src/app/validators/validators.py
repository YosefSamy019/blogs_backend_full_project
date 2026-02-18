import re

from typing import List, Optional


class Validators:
    EMAIL_REGEX = re.compile(
        r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    )

    def __init__(self):
        raise NotImplementedError(
            "You cant make objects from this class"
        )

    @staticmethod
    def validate_email(value: Optional[str]):
        if not value:
            raise ValueError("Email must be provided")
        if not Validators.EMAIL_REGEX.fullmatch(value):
            raise ValueError(f"Invalid email format: {value}")
        return None

    @staticmethod
    def validate_password(value: Optional[str]):
        if not value:
            raise ValueError("Password must be provided")
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one number")
        if not any(char.isalpha() for char in value):
            raise ValueError("Password must contain letters")
        return None

    @staticmethod
    def at_least_one_valid(values: List[Optional[str]]):
        # True if at least one value is not None or empty string
        cleaned_values = [v for v in values if v not in (None, "")]
        if not cleaned_values:
            raise ValueError("At least one field must be provided")
        return None
