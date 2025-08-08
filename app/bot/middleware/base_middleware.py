from typing import Any, Awaitable, Callable, Dict
from aiogram.fsm.middleware import BaseMiddleware  # type: ignore
from aiogram.types import TelegramObject, User, ChatMemberLeft

from app.core import load_config
from app.bot.keyboars.base_keyboards import url_to_channel
from app.bot.fonts.middleware_font import MiddlewareFont


settings = load_config()


class UserInChanel(BaseMiddleware):  #! ДОДЕЛАТЬ МИДЛТВАРЬ
    """Checks if the user is in the channels"""
    async def __call__(self,
                       handler: Callable[[TelegramObject,
                                          Dict[str, Any]],
                                         Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        user: User = data.get('event_from_user')  # type: ignore
        my_channel: str = settings.link.et_channel

        check_user = await event.bot.get_chat_member(my_channel, user.id) # type: ignore

        is_user_in_channel = not isinstance(check_user, ChatMemberLeft)

        if is_user_in_channel:
            await handler(event, data)
            return

        await event.bot.send_message(user.id,  # type: ignore
                                     MiddlewareFont.user_not_in_channel,
                                     reply_markup=url_to_channel)
        return