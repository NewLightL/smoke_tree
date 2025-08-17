from enum import Enum

from aiogram.filters.callback_data import CallbackData


class BasketAction(Enum):
    plus = "plus"
    minus = "minus"
    paginate = "paginate"
    home = "home"
    filter = "filter"
    reset = "reset"
    confirm = "confirm"


class BasketCallback(CallbackData, prefix="basket"):
    action: BasketAction
    page: int = 0
    product_id: int|None = None
    count: int = 1
