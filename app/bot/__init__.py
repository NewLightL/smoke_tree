__all__ = (
    "bot",
    "dp",
    "base_router",
    "catalog_router",
)

from app.bot.main import bot, dp
from app.bot.handlers.base import router as base_router
from app.bot.handlers.catalog import router as catalog_router
