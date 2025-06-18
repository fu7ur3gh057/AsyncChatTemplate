from typing import AsyncGenerator
from taskiq import TaskiqDepends

from redis.asyncio import Redis
from starlette.requests import Request


async def get_redis_pool(
    request: Request = TaskiqDepends(),
) -> AsyncGenerator[Redis, None]:  # pragma: no cover
    """
    Returns connection pool.

    You can use it like this:

    >>> from redis.asyncio import ConnectionPool, Redis
    >>>
    >>> async def handler(redis_pool: ConnectionPool = TaskiqDepends(get_redis_pool)):
    >>>     async with Redis(connection_pool=redis_pool) as redis:
    >>>         await redis.get('key')

    I use pools, so you don't acquire connection till the end of the handler.

    :param request: current request.
    :returns:  redis connection pool.
    """
    return request.app.state.redis_pool
