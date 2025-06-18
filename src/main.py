import uvicorn

from .core.settings import settings


def main() -> None:
    """Entrypoint of the application."""
    uvicorn.run(
        "src.web.application:get_app",
        workers=settings.WORKERS_COUNT,
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        proxy_headers=True,
        forwarded_allow_ips="*",
    )


if __name__ == "__main__":
    main()
