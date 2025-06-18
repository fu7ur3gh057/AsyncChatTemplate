from typing import AsyncGenerator

from firebase_admin import App as FirebaseApp
from starlette.requests import Request
from taskiq import TaskiqDepends


async def get_firebase_app(
    request: Request = TaskiqDepends(),
) -> AsyncGenerator[FirebaseApp, None]:
    return request.app.state.firebase_app
