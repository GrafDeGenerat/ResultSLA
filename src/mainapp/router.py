from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import ValidationError

from mainapp.schemas import RequestModel
from mainapp.service import calculate_deadline
from src.auth.utils import check_auth

router = APIRouter()


@router.post("/")
async def main(request_json=Depends(check_auth)) -> JSONResponse:
    try:
        request = RequestModel(**request_json)
    except ValidationError as e:
        logger.error(e)
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=f"Invalid body ({e})")
    result = calculate_deadline(request)
    return JSONResponse(status_code=status.HTTP_200_OK, content=result.json())
