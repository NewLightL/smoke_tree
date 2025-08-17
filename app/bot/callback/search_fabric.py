from enum import Enum

from aiogram.filters.callback_data import CallbackData

class SearchAction(Enum):
    select = "select"
    # apply = "apply"
    # reset = "reset"
    paginate = "paginate"
    filter = "filter"
    home = "home"
    basket = "basket"


class SearchCallback(CallbackData, prefix="search"):
    action: SearchAction
    product_id: int|None = None
    page: int = 0
