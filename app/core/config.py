from typing import Self

from pydantic_settings import SettingsConfigDict, BaseSettings


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env",
                                      extra="ignore",
                                      env_file_encoding="utf-8")

    @classmethod
    def load(cls) -> Self:
        return cls()



class Config(BaseConfig):
    pass


def load_config() -> Config:
    return Config.load()
