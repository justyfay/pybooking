from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_pass: str

    secret_key: str
    algorithm: str

    redis_host: str
    redis_port: int

    base_url: str

    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_password: str

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"

    @property
    def redis_url(self) -> str:
        return f"{self.redis_host}:{self.redis_port}"


settings = Settings()
