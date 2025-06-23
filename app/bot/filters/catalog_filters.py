from typing import Any

from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery


class CorrectColumn(BaseFilter):
    def __init__(self, values: list[str]):
        self.values = values


    async def __call__(self, call: CallbackQuery, *args: Any, **kwds: Any) -> Any:
        return call.data in self.values