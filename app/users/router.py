from fastapi import APIRouter, status
from app.users.schemas import SUserCreate, SUserInfo
from app.users.service import UserService

router_auth = APIRouter(
    prefix="/auth",
    tags=["Пользователи"]
)


@router_auth.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: SUserCreate) -> SUserInfo:
    return await UserService.service_register_user(user)
