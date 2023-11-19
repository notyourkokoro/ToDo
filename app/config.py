from functools import lru_cache
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent
ENV_PATH = BASE_DIR.joinpath('.env')


class PostgresSettings(BaseModel):
    name: str
    user: str
    password: str
    host: str
    port: int

    @property
    def url(self):
        return f'postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}'


class Settings(BaseSettings):
    postgres: PostgresSettings
    secret_auth: str

    model_config = SettingsConfigDict(env_file=ENV_PATH, env_file_encoding='UTF-8', env_nested_delimiter='__')


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
