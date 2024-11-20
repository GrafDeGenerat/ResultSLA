import json
import jwt
from loguru import logger
from config import settings
from datetime import datetime, timedelta
from db.database import check_username, check_user_id
from fastapi import Header, HTTPException, Depends, status
from fastapi.requests import Request
from fastapi.security import HTTPBasic, HTTPAuthorizationCredentials
from typing import Annotated, Optional

security = HTTPBasic()


async def identificate_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    user = check_username(credentials)

    if not user or user.password != credentials.password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    return {"id": user.id,
            "username": user.username
            }


def create_token(user: dict) -> str:
    expired = datetime.now() + timedelta(days=1)
    payload = {"sub": user,
               "exp": expired}
    token = jwt.encode(algorithm=settings.ALGORITHM,
                       payload=payload,
                       key=settings.SECRET_KEY,
                       )
    logger.debug(f"Creating token complete")
    return token


def check_token(token: str) -> dict:
    decoded = jwt.decode(jwt=token,
                         key=settings.SECRET_KEY,
                         algorithms=[settings.ALGORITHM])
    date_in_token = decoded["exp"]
    date_now = datetime.now().timestamp()

    if date_in_token < date_now:
        logger.warning(f'Token expired')
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Token expired. Try to get it at 'get_token' uri")

    logger.debug(f"Token decoded")
    return decoded


async def check_auth(request: Request,
                     token: Annotated[Optional[str], Header(description='Token')] = None,
                     ) -> dict:
    if not token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Token is missing. Try to get it at 'get_token' uri")

    in_token = check_token(token)
    user_from_token = in_token.get("sub")
    user = check_user_id(user_from_token.get("id"))

    if not user.username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="User not found")

    in_user = user_from_token.get("username")

    if user.username != in_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Wrong auth data")

    body = await request.body()

    if not body:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="Bad or empty request")

    res = json.loads(body.decode("utf-8"))
    return res
