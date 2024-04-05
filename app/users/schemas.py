from pydantic import BaseModel


class SUserBase(BaseModel):
    username: str


class SUserCreate(SUserBase):
    password: str


class SUserInfo(SUserBase):
    id: int
    hashed_password: str
