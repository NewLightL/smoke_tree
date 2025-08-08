__all__ = (
    "bot",
    "dp",
    "base_router",
    "catalog_router",
    "search_router",
    "UserInChanel"
)

from app.bot.main import bot, dp
from app.bot.handlers.base import router as base_router
from app.bot.handlers.catalog import router as catalog_router
from app.bot.handlers.search import router as search_router
from app.bot.middleware.base_middleware import UserInChanel
