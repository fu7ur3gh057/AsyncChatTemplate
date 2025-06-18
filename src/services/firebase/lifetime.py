from fastapi import FastAPI
from firebase_admin import credentials, initialize_app, delete_app

from src.core.settings import settings


def init_firebase(app: FastAPI) -> None:
    """
    Инициализация Firebase SDK и сохранение инстанса в app.state
    """
    cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
    firebase_app = initialize_app(cred)
    app.state.firebase_app = firebase_app


async def shutdown_firebase(app: FastAPI) -> None:
    """
    Завершение Firebase при остановке приложения
    """
    firebase_app = app.state.firebase_app
    delete_app(firebase_app)
