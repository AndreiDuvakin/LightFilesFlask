from password_generator import PasswordGenerator

from app.db.session import get_db
from app.models.user_model import UserModel
from app.services.users_service import UsersService


async def create_admin_user():
    async with get_db() as db:
        users_service = UsersService(db)

        users = await users_service.get_all()

        if users:
            return

        pwo = PasswordGenerator()
        pwo.minlen = 8
        pwo.maxlen = 8
        new_password = pwo.generate()

        user = UserModel(
            username="admin",
            password=new_password,
        )

        user = await users_service.create_user(user)

        print(f"New admin user. Login: {user.username}, Password: {new_password}")
