from app.features.users.models import User
from app.features.users.repository import UserDatabase


async def test_happy_user_add_to_db(db_session):
    user = User(
        username="test_user",
        email="test_user@test.py",
        password_hash="$argon2hashedpassword",
    )

    user_repository = UserDatabase()

    user = await user_repository.add_user_to_db(db_session, user)

    assert user.username == "test_user"
    assert user.email == "test_user@test.py"
    assert user.password_hash == "$argon2hashedpassword"