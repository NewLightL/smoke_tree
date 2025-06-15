from typing import Literal, Self

from pydantic_settings import SettingsConfigDict, BaseSettings


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env",
                                      extra="ignore",
                                      env_file_encoding="utf-8")

    @classmethod
    def load(cls) -> Self:
        return cls()


class CoreConfig(BaseConfig):
    mode: Literal["PROD", "DEV", "TEST"]
    log_level: int


class BotConfig(BaseConfig):
    bot_token: str
    admin_ids: list[int]

    # @property
    # def bot_token(self) -> str:
    #     return self.bot_token.replace(r"\x3a", ":")


class DBConfig(BaseConfig):
    db_host: str
    db_port: int
    db_user: str
    db_pass: str
    db_name: str

    @property
    def db_url(self) -> str:
        """Create a connection to the database"""
        return (
            f"postgresql+asyncpg://{self.db_user}"
            f":{self.db_pass}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


class APIConfig(BaseConfig):
    fastapi_host: str
    fastapi_port: int
    base_site: str
    secret_webhook: str

    @property
    def get_webhook_url(self) -> str:
        """Возвращает URL вебхука с кодированием специальных символов."""
        return f"{self.base_site}/webhook"


class TestConfig(BaseConfig):
    test_db_host: str
    test_db_port: int
    test_db_user: str
    test_db_pass: str
    test_db_name: str

    @property
    def db_url(self) -> str:
        """Create a connection to the database"""
        return (
            f"postgresql+asyncpg://{self.test_db_user}"
            f":{self.test_db_pass}"
            f"@{self.test_db_host}:{self.test_db_port}/{self.test_db_name}"
        )


class Config(BaseConfig):
    core: CoreConfig = CoreConfig.load()
    bot: BotConfig = BotConfig.load()
    db: DBConfig = DBConfig.load()
    api: APIConfig = APIConfig.load()
    test: TestConfig = TestConfig.load()


def load_config() -> Config:
    return Config.load()

print(load_config().core.log_level)
