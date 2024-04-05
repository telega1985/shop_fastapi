import json

from fastapi import Request

from app.config import settings
from redis import asyncio as aioredis

redis_connect = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")


class RedisTools:
    @classmethod
    async def get_session_id(cls, request: Request) -> str:
        session_id = request.cookies.get("session_id")
        if not session_id:
            session_id = await redis_connect.execute_command("INCR", "session_counter")

        return session_id

    @classmethod
    async def get_cart(cls, session_id: str) -> dict:
        cart_data = await redis_connect.get(f"cart:{session_id}")
        if cart_data:
            return json.loads(cart_data)

        return {}

    @classmethod
    async def save_cart(cls, session_id: str, cart: dict):
        cart_json = json.dumps(cart)
        await redis_connect.set(f"cart:{session_id}", cart_json)

    @classmethod
    async def get_cart_with_session_id(cls, request: Request):
        session_id = await cls.get_session_id(request)
        cart = await cls.get_cart(session_id)
        return session_id, cart

    @classmethod
    async def clear_cart(cls, session_id: str):
        await redis_connect.delete(f"cart:{session_id}")
