from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import user
from app.exceptions.base import (
    EmailAlreadyExistsError,
    UsernameAlreadyExistsError,
)
from app.schemas.user import UserCreate


class UserDatabase:
    @staticmethod
    def add_user_to_db(session: Session, user_data: UserCreate):
        try:
            statement_check_email = select(user.User).where(user.User.email == user_data.email)
            check_user_email_exists = session.scalar(statement_check_email)
            if check_user_email_exists is not None:
                raise EmailAlreadyExistsError

            statement_check_username = select(user.User).where(user.User.username == user_data.username)
            check_user_username_exists = session.scalar(statement_check_username)
            if check_user_username_exists is not None:
                raise UsernameAlreadyExistsError

            user_to_db = user.User(
                username=user_data.username,
                email=user_data.email,
                password_hash=user_data.password_hash,
            )

            session.add(user_to_db)
            session.commit()
            session.refresh(user_to_db)

            return user_to_db

        except Exception as e:
            session.rollback()
            raise e