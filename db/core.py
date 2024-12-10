from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker
)
from sqlalchemy import URL


def create_engine(url: URL) -> AsyncEngine:
    engine = create_async_engine(url)
    return engine


def create_async_session(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    session = async_sessionmaker(bind=engine, class_=AsyncSession)
    return session

