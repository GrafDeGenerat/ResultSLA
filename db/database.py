from config import settings as s
from db.db_schema import Base, Users
from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.types import Any
from schemas import UserModel
from sqlalchemy import create_engine, select, and_, Row
from sqlalchemy.orm import Session

engine = create_engine(f"{s.DB_TYPE}://{s.DB_USER}"
                       f"{':'+s.DB_PASS if s.DB_PASS else s.DB_PASS}"
                       f"@{s.DB_URL}:{s.DB_PORT}/"
                       f"{s.DB_NAME}?sslmode=disable",
                       echo=False
                       )


def create():
    Base.metadata.create_all(engine)


def check_username(in_user: HTTPAuthorizationCredentials) -> Row | None:
    stmt = select(Users.id,
                  Users.username,
                  Users.password
                  ).where(and_(Users.username == in_user.username)
                          )
    with Session(engine) as session:
        result = session.execute(stmt).fetchone()
        if result and result.password == in_user.password:
            return result
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not enough permissions",
                            )


def check_user_id(in_user: int) -> Row | None:
    stmt = select(Users.username).where(and_(Users.id == in_user))
    with Session(engine) as session:
        result = session.execute(stmt).fetchone()
        if result:
            return result
