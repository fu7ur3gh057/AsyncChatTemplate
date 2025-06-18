from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from db.models.key_model import KeyModel


class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = request.headers.get("X-API-Key")

        if not token:
            return JSONResponse({"detail": "X-API-Key header missing"}, status_code=401)

        key = await KeyModel.get_or_none(token=token)
        if not key:
            return JSONResponse({"detail": "Invalid API key"}, status_code=401)

        # При желании можешь прикрепить объект ключа к запросу:
        request.state.api_key = key

        return await call_next(request)
