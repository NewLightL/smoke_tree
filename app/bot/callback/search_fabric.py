from enum import Enum

from aiogram.filters.callback_data import CallbackData

from app.bot.callback.callback_core import Action


class SearchAction(Enum):
    select = "select"
    # apply = "apply"
    # reset = "reset"
    paginate = "paginate"
    filter = "filter"
    home = "home"
    admin = "admin"


class SearchCallback(CallbackData, prefix="search"):
    action: SearchAction
    product_id: int|None = None
    page: int = 0
