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
    value_str: str|None = None  # выбранное значение str
    value_int: int|None = None  # выбранное значение int
    value_float: float|None = None  # выбранное значение float
    value_bool: bool|None = None  # выбранное значение bool
    page: int = 0  # текущая страница
