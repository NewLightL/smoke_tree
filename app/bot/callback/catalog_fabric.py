from enum import Enum

from aiogram.filters.callback_data import CallbackData


class Action(str, Enum):
    select = "select"
    apply = "apply"
    reset = "reset"
    paginate = "paginate"


class CallbackProduct(CallbackData, prefix="products"):
    action: Action
    filter_type: str|None = None  # "taste", "brand" и т.д.
    value: int|float|bool|str|None = None  # выбранное значение
    page: int = 0  # текущая страница
