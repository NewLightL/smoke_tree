from typing import Any

from fastapi_storages.integrations.sqlalchemy import FileType as _FileType
from fastapi_storages import FileSystemStorage


class FileType(_FileType):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(storage=FileSystemStorage(path=r"app\static\photo"), *args, **kwargs)
