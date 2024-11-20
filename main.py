import sys
from typing import Annotated
from auth import create_token, check_auth, identificate_user
from config import settings
from db import database
from fastapi import FastAPI, status, Depends, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import ValidationError
from service import calculate_deadline
from schemas import RequestModel


app = FastAPI()

logger.remove()
logger.add(sys.stderr, level=settings.LOG_LEVEL)
database.create()


@app.post("/")
async def main(request_json: Annotated[dict, Depends(check_auth)]) -> JSONResponse:
    try:
        request = RequestModel(**request_json)
    except ValidationError as e:
        logger.error(e)
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid body ({e})")
    result = calculate_deadline(request)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=result.json())


@app.post("/get_token/")
async def get_token(user=Depends(identificate_user)) -> JSONResponse:
    result = create_token(user)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"access_token": result})

