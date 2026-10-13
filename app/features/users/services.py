from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.base import UnknownUserCreateError
from app.features.users.models import User
from app.features.users.repository import UserDatabase
from app.features.users.schemas import TokenResponse, UserCreate, UserLogin
from app.security.jwt import create_access_token
from app.security.password import hash_password


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user_data: UserCreate):
        password_hash = hash_password(user_data.password)

        user_data_to_db = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=password_hash,
        )

        created_user = await UserDatabase.add_user_to_db(self.session, user_data_to_db)

        if not created_user:
            raise UnknownUserCreateError

        return created_user

    async def login_user(self, user_data: UserLogin):
        user = await UserDatabase.check_user_login(self.session, user_data)

        token = await create_access_token(user.user_id)

        return TokenResponse(
            access_token=token,
            token_type="bearer",
        )