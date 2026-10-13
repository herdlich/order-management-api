import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer

from app.exceptions.base import UnauthorizedError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/auth")

load_dotenv("app/.env")

jwt_secret_key = os.getenv("JWT_SECRET_KEY")
jwt_algorithm = os.getenv("JWT_ALGORITHM")


async def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(hours=2)

    payload = {
        "sub": str(user_id),
        "exp": expire,
    }

    token = jwt.encode(payload, jwt_secret_key, algorithm=jwt_algorithm)

    return token


async def decode_access_token(token: str) -> int:
    try:
        payload = jwt.decode(token, jwt_secret_key, algorithms=[jwt_algorithm])

    except jwt.PyJWTError:
        raise UnauthorizedError

    user_id = payload.get("sub", None)

    if user_id is None or not user_id.isdigit():
        raise UnauthorizedError
    
    return int(user_id)