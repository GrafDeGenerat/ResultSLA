from fastapi import (APIRouter,
                     Depends,
                     status,
                     )
from fastapi.responses import JSONResponse

from src.auth.utils import identificate_user, create_token

router = APIRouter()


@router.post("/get_token/")
async def get_token(user=Depends(identificate_user)) -> JSONResponse:
    result = create_token(user)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"access_token": result})