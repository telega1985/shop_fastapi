from typing import Optional
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession


class BaseDAO:
    model = None

    @classmethod
    async def get_all(cls, session: AsyncSession, limit: Optional[int] = None):
        query = select(cls.model).limit(limit).order_by(-cls.model.id.desc())
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def get_one(cls, session: AsyncSession, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalars().one_or_none()

    @classmethod
    async def create(cls, session: AsyncSession, **data):
        query = insert(cls.model).values(**data).returning(cls.model)
        result = await session.execute(query)
        return result.scalars().one()

    @classmethod
    async def get_last(cls, session: AsyncSession):
        query = select(cls.model).order_by(cls.model.id.desc())
        result = await session.execute(query)
        return result.scalars().first()
