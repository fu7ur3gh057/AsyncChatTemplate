from pydantic import BaseModel


class FirebasePushOut(BaseModel):
    status: str  # "success", "error", "empty"
    message_id: str | None = None  # Только для send_notification
    success_count: int | None = None  # Только для send_multicast
    failure_count: int | None = None
    message: str | None = None  # Ошибка или описание
