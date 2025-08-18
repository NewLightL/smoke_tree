"""
poetry run uvicorn app.main:fastapi_app
"""
import logging

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from sqlalchemy import text
from sqladmin import Admin

from app.core import load_config, redis_backend
from app.bot import (
    dp,
    bot,
    base_router,
    catalog_router,
    search_router,
    basket_router,
    UserInChanel,
    RateLimitMiddleware
)
from app.api import webhook_router
from app.admin import (
    ProductsView,
    UsersView,
    OrdersView,
    OrdersProductsView,
    AuthAdmin,
)
from app.db.helper import helper
from app.api.templates.templates import templates


logging.getLogger("passlib").setLevel(logging.ERROR)


settings = load_config()


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with helper.engine.begin() as sess:
        await sess.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm"))
        await sess.commit()

    FastAPICache.init(RedisBackend(redis_backend), prefix="fastapi-cache")

    dp.include_router(catalog_router)
    dp.include_router(search_router)
    dp.include_router(basket_router)
    dp.include_router(base_router)
    dp.update.outer_middleware(UserInChanel())
    dp.message.middleware(RateLimitMiddleware())

    webhook_url = settings.api.get_webhook_url
    await bot.set_webhook(url=webhook_url,
                          allowed_updates=dp.resolve_used_update_types(),
                          drop_pending_updates=True,
                          secret_token=settings.api.secret_webhook)
    yield
    await bot.delete_webhook()


fastapi_app = FastAPI(lifespan=lifespan)

fastapi_app.mount(r"/static", StaticFiles(directory=settings.core.static_path), "static")

@fastapi_app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html"
    )

fastapi_app.include_router(webhook_router)

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.api.get_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=[],
)

admin = Admin(fastapi_app, helper.engine,
              authentication_backend=AuthAdmin(settings.api.jwt_key),
              templates_dir=r"app\api\templates\admin")

admin.add_view(ProductsView)
admin.add_view(UsersView)
admin.add_view(OrdersView)
admin.add_view(OrdersProductsView)
