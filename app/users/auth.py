from passlib.context import CryptContext
from datetime import datetime, timedelta, UTC
from jose import jwt

from app.config import settings
from app.database import async_session_maker
from app.exceptions import IncorrectEmailOrPasswordException
from app.users.dao import UserDAO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    @classmethod
    def get_password_hash(cls, password: str) -> str:
        return pwd_context.hash(password)

    @classmethod
    def verify_password(cls, plain_password, hashed_password) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def create_access_token(cls, user_id: int) -> str:
        to_encode = {
            "sub": str(user_id),
            "exp": datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        }
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)

        return encoded_jwt

    @classmethod
    async def authenticate_user(cls, username: str, password: str):
        async with async_session_maker() as session:
            db_user = await UserDAO.get_one(session, username=username)

        if not (db_user and cls.verify_password(password, db_user.hashed_password)):
            raise IncorrectEmailOrPasswordException

        return db_user
