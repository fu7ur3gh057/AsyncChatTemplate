import asyncio

from firebase_admin import messaging, App

from core.logger import logger
from src.services.firebase.schemas import FirebasePushOut


class FirebaseUtils:
    def __init__(self, app: App):
        self.app = app

    async def send_notification(
        self,
        token: str,
        title: str,
        body: str,
        data: dict[str, str] | None = None,
    ) -> FirebasePushOut:
        try:
            message = messaging.Message(
                notification=messaging.Notification(title=title, body=body),
                token=token,
                data=data or {},
            )
            response = await asyncio.to_thread(messaging.send, message, app=self.app)
            logger.info(f"Push sent to {token}: {response}")
            return FirebasePushOut(status="success", message_id=response)
        except Exception as e:
            logger.error(f"Push send failed: {e}")
            return FirebasePushOut(status="error", message=str(e))

    async def send_multicast(
        self,
        tokens: list[str],
        title: str,
        body: str,
        data: dict[str, str] | None = None,
    ) -> FirebasePushOut:
        if not tokens:
            logger.warning("No tokens to send push")
            return FirebasePushOut(status="empty", success_count=0, failure_count=0)

        try:
            messages = [
                messaging.Message(
                    token=token,
                    notification=messaging.Notification(title=title, body=body),
                    data=data or {},
                )
                for token in tokens
            ]

            responses = await asyncio.to_thread(
                messaging.send_each, messages, app=self.app
            )

            success = sum(1 for r in responses if r.success)
            failure = len(responses) - success

            for idx, r in enumerate(responses):
                if not r.success and "not registered" in str(r.exception).lower():
                    logger.warning(f"Unregistered token: {tokens[idx]}")
                    # Токен можно деактивировать тут

            return FirebasePushOut(
                status="success",
                success_count=success,
                failure_count=failure,
            )
        except Exception as e:
            logger.error(f"Multicast push failed: {e}")
            return FirebasePushOut(status="error", message=str(e))
