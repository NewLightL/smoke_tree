from datetime import datetime, timezone

from fastapi import Depends, Request
from jose import JWTError, jwt

import app.core.excepction.auth as ex_auth
from app.core import load_config


settings = load_config()

def get_token(request: Request):
    token = request.cookies.get("admin_access_token")
    if not token:
        raise ex_auth.TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        decode_jwt = jwt.decode(token, settings.api.jwt_key, settings.api.jwt_alghoritm)
    except JWTError:
        raise ex_auth.TokenIncorrectFormatException

    expire: str | None = decode_jwt.get("exp")
    if not expire or int(expire) < datetime.now(timezone.utc).timestamp():
        raise ex_auth.TokenExpiredException

    user_id: int | None = int(decode_jwt.get("sub"))
    if not user_id or user_id not in settings.bot.admin_ids:
        raise ex_auth.UserException

    return user_id
