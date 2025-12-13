import redis.asyncio as aioredis

from src.utils.config import settings



token_block_list = aioredis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
    socket_connect_timeout=10
)


async def add_token_to_blocklist(token_id: str):
    return await token_block_list.set(name=token_id, value="removed", ex=settings.TOKEN_EXP)


async def get_token_in_blocklist(token_id: str):
    token_id_exists = await token_block_list.get(token_id)
    print(f"{token_id_exists = }")
    return token_id_exists