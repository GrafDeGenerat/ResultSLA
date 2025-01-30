from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


def create_engine(url: URL) -> AsyncEngine:
    engine = create_async_engine(url)
    return engine


def create_async_session(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    session = async_sessionmaker(bind=engine, class_=AsyncSession)
    return session
