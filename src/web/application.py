import logging

import sentry_sdk
from fastapi import FastAPI, HTTPException
from fastapi.responses import UJSONResponse
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from starlette.middleware.cors import CORSMiddleware

from src.core.exceptions import AppException
from src.core.settings import settings
from src.web.api.router import api_router
from src.web.lifetime import lifespan
from web.middlewares import APIKeyMiddleware


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    if settings.SENTRY_DNS:
        sentry_sdk.init(
            dsn=settings.SENTRY_DNS,
            traces_sample_rate=settings.SENTRY_SAMPLE_RATE,
            environment=settings.ENVIRONMENT,
            integrations=[
                FastApiIntegration(transaction_style="endpoint"),
                LoggingIntegration(
                    level=logging.getLevelName(settings.LOG_LEVEL),
                    event_level=logging.ERROR,
                ),
                SqlalchemyIntegration(),
            ],
            send_default_pii=True,
        )
    application = FastAPI(
        title="Chat App",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
        lifespan=lifespan,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Content-Security-Policy"],
    )
    application.add_middleware(APIKeyMiddleware)

    @application.exception_handler(AppException)
    async def custom_exception_handler(request, exc: AppException):
        raise HTTPException(status_code=exc.status_code, detail=exc.detail)

    # Main router for the API.
    application.include_router(router=api_router, prefix="/api")
    return application
