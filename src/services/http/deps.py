from typing import AsyncGenerator

import aiohttp
from starlette.requests import Request


async def get_http_session(
    request: Request,
) -> AsyncGenerator[aiohttp.ClientSession, None]:
    return request.app.state.aiohttp_session
