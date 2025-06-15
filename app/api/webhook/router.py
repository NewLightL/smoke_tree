from fastapi import APIRouter, Request
from aiogram.types import Update

from app.bot import dp, bot


router = APIRouter(prefix="/webhook", tags=["webhook"])


@router.post("")
async def webhook(request: Request) -> None:
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)
