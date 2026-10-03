import os
from collections.abc import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

load_dotenv("app"/".env")

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError('!!! No found "DATABASE_URL" in .env file !!!')

engine = create_engine(DATABASE_URL)
SessionFactory = sessionmaker(bind=engine)


def get_session() -> Generator[Session, None, None]:
    session = SessionFactory()

    try:
        yield session
    finally:
        session.close()