from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy import select, and_, Row

from src.config import Settings
from src.db.models import Users
from src.db.core import create_engine, create_async_session

s = Settings.get_settings()
engine = create_engine(url=s.db.DB_URL)


async def check_username(in_user: HTTPAuthorizationCredentials) -> Row | None:
    stmt = select(Users.id,
                  Users.username,
                  Users.password
                  ).where(and_(Users.username == in_user.username))
    session = create_async_session(engine)
    async with session.begin() as session:
        db_result = (await session.execute(stmt)).fetchone()

        if db_result and db_result.password == in_user.password:
            return db_result
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not enough permissions",
                            )


async def check_user_id(in_user: int) -> Row | None:
    stmt = select(Users.username).where(and_(Users.id == in_user))
    session = create_async_session(engine)
    async with session.begin() as session:
        result = (await session.execute(stmt)).fetchone()
        return result

