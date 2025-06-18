from typing import AsyncGenerator

from socketio import ASGIApp, AsyncServer
from starlette.requests import Request


async def get_sio_app(
    request: Request,
) -> AsyncGenerator[ASGIApp, None]:
    return request.app.state.sio_app


async def get_sio_server(
    request: Request,
) -> AsyncGenerator[AsyncServer, None]:
    return request.app.state.sio_server
