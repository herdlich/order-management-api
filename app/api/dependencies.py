from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.services.user import UserService


def get_user_service(session: Annotated[Session, Depends(get_session)]) -> UserService:
    return UserService(session)