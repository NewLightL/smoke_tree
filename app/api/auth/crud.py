from typing import Any

from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt

from app.core import load_config


settings = load_config()


class AuthCrud:
    context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def verify_login_and_password(cls, login: int, password: str) -> bool:
        is_correct_login = login in settings.bot.admin_ids
        is_correct_password = cls.context.verify(password, settings.bot.password)
        return is_correct_login and is_correct_password

    @classmethod
    def create_token(cls, data: dict[str, Any]) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            settings.api.jwt_key,
            settings.api.jwt_alghoritm)
        return encoded_jwt
