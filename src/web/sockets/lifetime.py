import socketio
from fastapi import FastAPI

from src.core.settings import settings
from src.web.ws.namespaces.drivers.namespace import DriverNamespace
from src.web.ws.namespaces.orders.namespace import OrderNamespace


async def init_socketio(app: FastAPI) -> None:
    sio_server = socketio.AsyncServer(
        async_mode="asgi",
        cors_allowed_origins=[],
    )

    sio_app = socketio.ASGIApp(
        socketio_server=sio_server,
        socketio_path=settings.WS_PATH,
    )

    async def _connect(sid, environ):
        print(f"global connect {sid}")

    async def _disconnect(sid):
        print(f"global disconnect {sid}")

    # Global Events
    sio_server.on(event="connect", handler=_connect)
    sio_server.on(event="disconnect", handler=_disconnect)
    sio_server.register_namespace(
        OrderNamespace(namespace=settings.ORDER_NAMESPACE_PATH, app=app)
    )
    sio_server.register_namespace(
        DriverNamespace(namespace=settings.DRIVER_NAMESPACE_PATH, app=app)
    )
    # Save state and mount to FastAPI app
    app.state.sio_server = sio_server
    app.state.sio_app = sio_app
    app.mount("/ws", app=sio_app)


async def shutdown_socketio(app: FastAPI) -> None:
    return None
