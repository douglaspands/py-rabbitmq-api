from functools import cache

from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    pass


@cache
def session_maker():
    pass


def get_session():
    pass


__all__ = ("session_maker", "get_session")
