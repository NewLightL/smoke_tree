from fastapi import status

from app.core.excepction.base import BaseException


class UserException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Ошибка пользователя"

class UserWrongPasswordOrLoginException(UserException):
    detail = "Неверный пароль или логин"

class UserWrongTypeException(UserException):
    status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
    detail = "неверный формат данных"


class TokenException(BaseException):
    status_code: int = status.HTTP_401_UNAUTHORIZED
    detail: str = "Ошибка токена"

class TokenExpiredException(TokenException):
    detail = "Истек токен"

class TokenAbsentException(TokenException):
    detail = "Токен отсутствует"

class TokenIncorrectFormatException(TokenException):
    detail = "Неверный формат токена"
