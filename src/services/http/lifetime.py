import aiohttp
from fastapi import FastAPI


def init_aiohttp(app: FastAPI) -> None:
    app.state.aiohttp_session = aiohttp.ClientSession()


async def shutdown_aiohttp(app: FastAPI) -> None:
    await app.state.aiohttp_session.close()
