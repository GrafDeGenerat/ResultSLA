from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import ValidationError

from src.mainapp.schemas import RequestModel
from src.mainapp.service import calculate_deadline

router = APIRouter()


@router.post("/")
async def main(request_json: dict) -> JSONResponse:
    try:
        request = RequestModel(**request_json)
    except ValidationError as e:
        logger.error(e)
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=f"Invalid body ({e})")
    result = calculate_deadline(request)
    logger.debug(f"result ready: {result.json()})")
    return JSONResponse(status_code=status.HTTP_200_OK, content=result.json())
