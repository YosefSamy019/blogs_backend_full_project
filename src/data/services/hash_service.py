class HashService:
    def __init__(self):
        pass

    def hash(self, password: str) -> str:
        return password[0::2] + password[1::2]

    def verify(self, password: str, hashed: str) -> bool:
        return self.hash(password) == hashed
