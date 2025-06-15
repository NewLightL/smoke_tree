from typing import Any

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from app.core import load_config


settings = load_config()

class Helper():
    def __init__(self, url: str, params: dict[str, Any]) -> None:
        self.engine = create_async_engine(url, **params)
        self.sessionf = async_sessionmaker(self.engine,
                                           autoflush=False,
                                           expire_on_commit=False,
                                           class_=AsyncSession)


url: str = settings.db.db_url
db_params: dict[str, Any] = {}

if settings.core.mode == "TEST":
    url = settings.test.db_url
    db_params = {"poolclass": NullPool}

helper = Helper(url, db_params)