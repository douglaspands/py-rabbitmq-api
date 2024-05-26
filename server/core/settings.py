from functools import cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # app
    app_name: str = "rabbitmq-api"
    app_help: str = "cli do consumer do rabbitmq"
    app_version: str = "0.1.0"

    # worker
    queue_host: str = ""
    queue_port: str = "5672"
    queue_name: str = ""
    queue_exchange: str = ""
    queue_routing_key: str = ""
    queue_username: str = ""
    queue_password: str = ""

    # database
    # db_debug: bool = False
    # db_url: str = Field(default=None)

    # config
    model_config = SettingsConfigDict(env_file=".env")


@cache
def get_settings() -> Settings:
    return Settings()


__all__ = ("Settings", "get_settings")
