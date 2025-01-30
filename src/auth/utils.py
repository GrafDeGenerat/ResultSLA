import json
from datetime import datetime, timedelta
from typing import Annotated, Optional

import jwt
from asyncpg.exceptions import (
    InvalidAuthorizationSpecificationError,
    InvalidCatalogNameError,
)
from fastapi import Depends, Header, HTTPException, status
from fastapi.requests import Request
from fastapi.security import HTTPBasic
from loguru import logger

from src.config import Settings
from src.db.exceptions import (
    DatabaseAuthException,
    DatabaseConnectionException,
    NoDatabaseException,
)
from src.db.utils import check_user_id, check_username

security = HTTPBasic()
settings = Settings.get_settings()


async def identificate_user(credentials=Depends(security)) -> dict:
    try:
        user = await check_username(credentials)
    except InvalidAuthorizationSpecificationError:
        raise DatabaseAuthException("Authentication to DB failed")
    except InvalidCatalogNameError:
        raise NoDatabaseException("Wrong DB name or no DB created")

    if not user or user.password != credentials.password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    return {"id": user.id, "username": user.username}


def create_token(user: dict) -> str:
    expired = datetime.now() + timedelta(days=1)
    payload = {"sub": user, "exp": expired}
    token = jwt.encode(
        algorithm=settings.app.ALGORITHM,
        payload=payload,
        key=settings.app.SECRET_KEY,
    )
    logger.debug("Creating token complete")
    return token


def check_token(token: str) -> dict:
    try:
        decoded = jwt.decode(
            jwt=token, key=settings.app.SECRET_KEY, algorithms=[settings.app.ALGORITHM]
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token expired. Try to get it at 'get_token' uri",
        )

    logger.debug("Token decoded")
    return decoded


async def check_auth(
    request: Request,
    token: Annotated[Optional[str], Header(description="Token")] = None,
) -> dict:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token is missing. Try to get it at 'get_token' uri",
        )

    in_token = check_token(token)
    user_from_token = in_token.get("sub")
    try:
        user = await check_user_id(user_from_token.get("id"))
    except ConnectionRefusedError:
        raise DatabaseConnectionException("No database connection could be established.")

    if not user.username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    in_user = user_from_token.get("username")

    if user.username != in_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong auth data"
        )

    body = await request.body()

    if not body:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Bad or empty request"
        )

    res = json.loads(body.decode("utf-8"))
    return res
