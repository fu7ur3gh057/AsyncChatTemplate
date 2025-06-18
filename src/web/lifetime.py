from contextlib import asynccontextmanager

from fastapi import FastAPI
from prometheus_fastapi_instrumentator.instrumentation import (
    PrometheusFastApiInstrumentator,
)

from services.firebase.lifetime import init_firebase, shutdown_firebase
from services.http.lifetime import init_aiohttp, shutdown_aiohttp
from services.redis.lifetime import init_redis, shutdown_redis
from web.sockets.lifetime import shutdown_socketio, init_socketio
from worker.lifetime import init_worker, shutdown_worker
from worker.tkq import broker


def _setup_prometheus(app: FastAPI) -> None:  # pragma: no cover
    """
    Enables prometheus integration.

    :param app: current application.
    """
    PrometheusFastApiInstrumentator(should_group_status_codes=False).instrument(
        app,
    ).expose(app, should_gzip=True, name="metrics")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager to set up database session factory.
    """
    init_redis(app)
    await init_worker(broker)
    await init_socketio(app)
    init_firebase(app)
    init_aiohttp(app)
    # _setup_prometheus(app)

    yield

    await shutdown_worker(broker)
    await shutdown_redis(app)
    await shutdown_socketio(app)
    await shutdown_firebase(app)
    await shutdown_aiohttp(app)
