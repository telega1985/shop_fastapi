from app.database import async_session_maker
from app.exceptions import UserAlreadyExistsException, UserNotFound
from app.users.auth import AuthService
from app.users.dao import UserDAO
from app.users.schemas import SUserCreate, SUserInfo


class UserService:
    @classmethod
    async def service_get_authorization_user(cls, user_id: int):
        async with async_session_maker() as session:
            db_user = await UserDAO.get_one(session, id=user_id)

        if not db_user:
            raise UserNotFound

        return db_user

    @classmethod
    async def service_register_user(cls, user: SUserCreate) -> SUserInfo:
        async with async_session_maker() as session:
            existing_user = await UserDAO.get_one(session, username=user.username)

            if existing_user:
                raise UserAlreadyExistsException

            hashed_password = AuthService.get_password_hash(user.password)

            db_user = await UserDAO.create(
                session,
                **user.model_dump(exclude={"password"}),
                hashed_password=hashed_password
            )

            await session.commit()

        return db_user
