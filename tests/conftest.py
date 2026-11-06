import pytest
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from pathlib import Path

from app.db.base import Base
from app.features.users import models as us_models
from app.features.products import models as prod_models
from app.features.orders import models as ord_models
from app.features.carts import models as cart_models
from app.features.cart_items import models as cart_i_models

ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / "app" / ".env")


@pytest.fixture
async def test_engine():
    database_test_url = os.getenv("DATABASE_TEST_URL")

    if not database_test_url:
        raise RuntimeError("DATABASE_TEST_URL not set")

    engine = create_async_engine(database_test_url)

    yield engine

    await engine.dispose()


@pytest.fixture
async def prepare_db(test_engine):
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session(test_engine, prepare_db):
    SessionFactory = async_sessionmaker(
        bind=test_engine,
        expire_on_commit=False,
    )

    async with SessionFactory() as session:
        yield session
