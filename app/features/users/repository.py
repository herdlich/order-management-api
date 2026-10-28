from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.base import (
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    UnauthorizedError,
    UsernameAlreadyExistsError,
)
from app.features.users.models import User
from app.features.users.schemas import UserLogin
from app.security.password import verify_password


class UserDatabase:
    @staticmethod
    async def add_user_to_db(session: AsyncSession, user_model: User) -> User:
        try:
            statement_check_email = select(User).where(User.email == user_model.email)
            check_user_email_exists = await session.scalar(statement_check_email)
            if check_user_email_exists is not None:
                raise EmailAlreadyExistsError

            statement_check_username = select(User).where(User.username == user_model.username)
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
    async def check_user_login(session: AsyncSession, user_model: UserLogin) -> User | None:
        statement_check_username = select(User).where(User.username == user_model.username)
        user_exists = await session.scalar(statement_check_username)

        if user_exists is None or not verify_password(
            user_model.password, 
            user_exists.password_hash
        ):
            raise InvalidCredentialsError

        return user_exists

    @staticmethod
    async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
        statement_user = select(User).where(User.user_id == user_id)
        user_exists = await session.scalar(statement_user)

        if user_exists is None:
            raise UnauthorizedError

        return user_exists