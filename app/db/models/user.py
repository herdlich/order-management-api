from pathlib import Path

ROOT_PATH = Path(__file__).parent.resolve().parents[2]

from datetime import datetime

from sqlalchemy import CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(unique=True, nullable=False)

    email: Mapped[str] = mapped_column(unique=True, nullable=False)

    password_hash = Mapped[str]

    role: Mapped[str] = mapped_column(nullable=False, default="user")
    
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    __table_args__ = (
        CheckConstraint(
            "role IN ('user', 'admin')",
            name="check_valid_user_roles",
        ),
    )
