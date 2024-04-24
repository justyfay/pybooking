from enum import Enum
from typing import List, Literal, Union

from pydantic_settings import BaseSettings, SettingsConfigDict


class Unset(Enum):
    token = 0

    def __repr__(self) -> str:
        return "UNSET"

    def __str__(self) -> str:
        return "UNSET"


UNSET = Unset.token


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    mode: Literal["Dev", "Test", "Prod"]
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_pass: str

    test_db_host: Union[str, Unset] = UNSET
    test_db_port: Union[int, Unset] = UNSET
    test_db_name: Union[str, Unset] = UNSET
    test_db_user: Union[str, Unset] = UNSET
    test_db_pass: Union[str, Unset] = UNSET

    secret_key: str
    algorithm: str

    redis_host: str
    redis_port: int

    sentry_dsn: str

    base_url: str
    origins: List[str]

    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_password: str

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"

    @property
    def database_test_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.test_db_user}:{self.test_db_pass}"
            f"@{self.test_db_host}:{self.test_db_port}/{self.test_db_name}"
        )

    @property
    def redis_url(self) -> str:
        return f"{self.redis_host}:{self.redis_port}"


settings = Settings()
