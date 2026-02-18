class Failure(Exception):
    def __init__(self, error_code: int, error_msg: str) -> None:
        self.error_code = error_code
        self.error_msg = error_msg

    def __str__(self) -> str:
        return f'{self.error_code}: {self.error_msg}'

    @classmethod
    def handle_error(cls, error) -> 'Failure':
        if isinstance(error, Failure):
            return error
        else:
            # Raise errors in case of debug only
            # raise error
            return cls(501, str(error))

    @classmethod
    def user_not_found(cls, user_id: int) -> 'Failure':
        return cls(404, f'User not found with ID {user_id}')

    @classmethod
    def user_not_found_with_email(cls, email: str) -> 'Failure':
        return cls(404, f'User not found with email {email}')

    @classmethod
    def blog_not_found(cls, blog_id: int) -> 'Failure':
        return cls(404, f'Blog not found with ID {blog_id}')

    @classmethod
    def wrong_password(cls) -> 'Failure':
        return cls(401, f'Invalid credentials')

    @classmethod
    def duplicated_email(cls, email: str) -> 'Failure':
        return cls(409, f'Email {email} already exists')

    @classmethod
    def wrong_access_token(cls) -> 'Failure':
        return cls(401, f'Invalid or expired access token')
