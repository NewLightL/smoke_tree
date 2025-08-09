from fastapi import HTTPException


class BaseException(HTTPException):
    status_code: int
    detail: str

    def __init__(self) -> None:
        super().__init__(self.status_code, self.detail)
