from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import Response

import app.core.excepction.auth as ex_auth
from app.api.auth.crud import AuthCrud
from app.api.auth.check_token import get_current_user


class AuthAdmin(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        try:
            login: int = int(form["username"])
            users_password: str = str(form["password"])
        except:
            raise ex_auth.UserWrongTypeException

        existing_user: bool = AuthCrud.verify_login_and_password(login, users_password)
        if existing_user:
            access_token = AuthCrud.create_token({"sub": str(login)})
            request.session.update({"token": access_token})

        return True

    async def logout(self, request: Request) -> Response | bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Response | bool:
        token = request.session.get("token")

        if not token:
            return False

        user_id = await get_current_user(token)
        if not user_id:
            return False

        # Check the token in depth
        return True
