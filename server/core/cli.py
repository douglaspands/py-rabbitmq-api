from typer import Typer

from server.core.settings import get_settings


def create_app() -> Typer:
    settings = get_settings()
    app = Typer(name=settings.app_name, help=settings.app_help)
    return app


__all__ = ("create_app",)
