from dotenv import dotenv_values


class Env:
    _instance = None
    _config = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._config = dotenv_values(".env")
        return cls._instance

    def is_debug(self) -> bool:
        return self._config.get("IS_DEBUG", "0") == "1"

    def sql_alchemy_db_url(self) -> str:
        return self._config.get("SQL_ALCHEMY_DB_URL")

    def sql_alchemy_echo(self) -> bool:
        return self._config.get("SQL_ALCHEMY_DB_ECHCO") == "1"

    def secret_key(self) -> str:
        return self._config.get("SECRET_KEY")

    def algorithm(self) -> str:
        return self._config.get("ALGORITHM")

    def page_size(self) -> int:
        return int(self._config.get("PAGE_SIZE"))
