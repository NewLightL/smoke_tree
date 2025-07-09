"""
poetry run uvicorn app.main:fastapi_app
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text

from app.core import load_config
from app.bot import dp, bot, base_router, catalog_router, search_router
from app.api import webhook_router
from app.db.helper import helper


settings = load_config()

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with helper.engine.begin() as sess:
        await sess.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm"))
        await sess.commit()
    dp.include_router(catalog_router)
    dp.include_router(search_router)
    dp.include_router(base_router)
    webhook_url = settings.api.get_webhook_url
    await bot.set_webhook(url=webhook_url,
                          allowed_updates=dp.resolve_used_update_types(),
                          drop_pending_updates=True,
                          secret_token=settings.api.secret_webhook)
    yield
    await bot.delete_webhook()


fastapi_app = FastAPI(lifespan=lifespan)

fastapi_app.mount(r"/static", StaticFiles(directory=settings.core.static_path), "static")

fastapi_app.include_router(webhook_router)
