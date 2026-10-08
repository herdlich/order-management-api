from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import user
from app.exceptions.base import (
    EmailAlreadyExistsError,
    UsernameAlreadyExistsError,
)
from app.schemas.user import UserCreate


class UserDatabase:
    @staticmethod
    async def add_user_to_db(session: AsyncSession, user_model: UserCreate):
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