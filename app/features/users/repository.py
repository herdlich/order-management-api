from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.base import (
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    UnauthorizedError,
    UsernameAlreadyExistsError,
)
from app.features.users import models as user
from app.features.users.schemas import UserCreate, UserLogin
from app.security.password import verify_password


class UserDatabase:
    @staticmethod
    async def add_user_to_db(session: AsyncSession, user_model: UserCreate) -> UserCreate:
        try:
            statement_check_email = select(user.User).where(user.User.email == user_model.email)
            check_user_email_exists = await session.scalar(statement_check_email)
            if check_user_email_exists is not None:
                raise EmailAlreadyExistsError

            statement_check_username = select(user.User).where(user.User.username == user_model.username)
            check_user_username_exists = await session.scalar(statement_check_username)
            if check_user_username_exists is not None:
                raise UsernameAlreadyExistsError

            session.add(user_model)
            await session.commit()
            await session.refresh(user_model)

            return user_model

        except Exception as e:
            await session.rollback()
            raise e

    @staticmethod
    async def check_user_login(session: AsyncSession, user_model: UserLogin) -> user.User:
        statement_check_username = select(user.User).where(user.User.username == user_model.username)
        user_exists = await session.scalar(statement_check_username)

        if user_exists is None or not verify_password(
            user_model.password, 
            user_exists.password_hash
        ):
            raise InvalidCredentialsError

        return user_exists

    @staticmethod
    async def get_user_by_id(session: AsyncSession, user_id: int) -> user.User:
        statement_user = select(user.User).where(user.User.user_id == user_id)
        user_exists = await session.scalar(statement_user)

        if user is None:
            raise UnauthorizedError

        return user_exists