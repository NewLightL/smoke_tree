from typing import Any, Awaitable, Callable
from datetime import timedelta, datetime, timezone
from collections import defaultdict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery

from app.bot.middleware.utils.async_timed_queue import AsyncTimedQueue
from app.bot.fonts.middleware_font import MiddlewareFont


class RateLimitMiddleware(BaseMiddleware):
    def __init__(self,
                 rate_limit: int = 5,
                 time_interval: timedelta = timedelta(seconds=10)) -> None:
        self.rate_limit = rate_limit
        self.time_interval = time_interval
        self.last_messages_ts = defaultdict[int, AsyncTimedQueue[datetime]](
            lambda: AsyncTimedQueue(max_age=time_interval)
        )

    async def __call__(self,  # type: ignore
                       handler: Callable[[TelegramObject,
                                          dict[str, Any]],
                                         Awaitable[Any]],
                       event: Message,
                       data: dict[str, Any]) -> Any:
        user_id: int = event.from_user.id
        last_messages = self.last_messages_ts[user_id]
        current_dt = datetime.now(timezone.utc)
        count: int = await last_messages.get_len()

        if count > self.rate_limit:
            return

        await last_messages.push(current_dt)

        count: int = await last_messages.get_len()
        if count == self.rate_limit:
            await event.answer(MiddlewareFont.rate_limit_is_over)
            return

        return await handler(event, data)


class RateLimitCallMiddleware(BaseMiddleware):
    def __init__(self,
                rate_limit: int = 10,
                time_interval: timedelta = timedelta(seconds=10)) -> None:
        self.rate_limit = rate_limit
        self.time_interval = time_interval
        self.last_messages_ts = defaultdict[int, AsyncTimedQueue[datetime]](
            lambda: AsyncTimedQueue(max_age=time_interval)
        )


    async def __call__(self,  # type: ignore
                       handler: Callable[[TelegramObject,
                                          dict[str, Any]],
                                         Awaitable[Any]],
                       event: CallbackQuery,
                       data: dict[str, Any]) -> Any:
        user_id: int = event.from_user.id
        last_messages = self.last_messages_ts[user_id]
        current_dt = datetime.now(timezone.utc)
        count: int = await last_messages.get_len()

        if count > self.rate_limit:
            return

        await last_messages.push(current_dt)

        count: int = await last_messages.get_len()
        if count == self.rate_limit:
            await event.answer(MiddlewareFont.rate_limit_is_over)
            return

        return await handler(event, data)
