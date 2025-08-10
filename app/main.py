"""
poetry run uvicorn app.main:fastapi_app
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text
from sqladmin import Admin

from app.core import load_config
from app.bot import (
    dp,
    bot,
    base_router,
    catalog_router,
    search_router,
    UserInChanel,
)
from app.api import webhook_router
from app.admin import (
    ProductsView,
    OrdersView,
    UsersView,
    OrdersProductsView,
    AuthAdmin
)
from app.db.helper import helper
from app.api.templates.templates import templates


settings = load_config()

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with helper.engine.begin() as sess:
        await sess.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm"))
        await sess.commit()

    dp.include_router(catalog_router)
    dp.include_router(search_router)
    dp.include_router(base_router)
    dp.update.outer_middleware(UserInChanel())

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

admin = Admin(fastapi_app, helper.engine,
              authentication_backend=AuthAdmin(settings.api.jwt_key))

admin.add_view(ProductsView)
admin.add_view(OrdersView)
admin.add_view(OrdersProductsView)
admin.add_view(UsersView)
