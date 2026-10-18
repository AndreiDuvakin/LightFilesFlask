from quart_auth import login_user

from app.db.session import get_db
from app.models.auth_model import AuthModel
from app.models.login_result_model import LoginResultModel
from app.services.users_service import UsersService


class AuthController:
    @staticmethod
    async def login(
        username: str,
        password: str,
        remember_me: bool,
    ) -> LoginResultModel:
        async with get_db() as db:
            users_service = UsersService(db)
            user = await users_service.check_login(username, password)

        if user is None:
            return LoginResultModel(
                success=False, error="Неправильный логин или пароль"
            )

        login_user(
            AuthModel(str(user.id)),
            remember_me,
        )
        return LoginResultModel(success=True)
