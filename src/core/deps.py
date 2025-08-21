from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import settings
from src.core.db import engine

async_engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, echo=False)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)


def async_session_maker():
    return async_sessionmaker(async_engine, expire_on_commit=False)()


async def get_async_session() -> AsyncIterator[AsyncSession]:
    async with async_session() as session:
        yield session


def get_sync_session():
    sync_session = sessionmaker(engine)  # noqa
    with sync_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_async_session)]
