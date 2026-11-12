from app.features.users.repository import UserDatabase
from app.features.users.schemas import UserCreate
from app.features.users.services import UserService


async def test_happy_user_create_service(db_session):
    user_to_create = UserCreate(
        username="test_user",
        email="test_user@test.py",
        password="qwerty",
    )
    user_repository = UserDatabase()

    user_service = UserService(db_session, user_repository)

    user = await user_service.create_user(user_to_create)

    assert user.username == "test_user"
    assert user.email == "test_user@test.py"
    assert user.password_hash != user_to_create.password
