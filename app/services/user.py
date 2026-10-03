from sqlalchemy.orm import Session

from app.db.models.user import User
from app.exceptions.base import UnknownUserCreateError
from app.repositories.user import UserDatabase
from app.schemas.user import UserCreate
from app.security.password import hash_password


class UserService:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user_data: UserCreate):
        password_hash = hash_password(user_data.password)

        user_data_to_db = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=password_hash,
        )

        created_user = UserDatabase.add_user_to_db(self.session, user_data_to_db)

        if not created_user:
            raise UnknownUserCreateError

        return created_user