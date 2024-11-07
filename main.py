import sys
from fastapi import FastAPI, status
from loguru import logger
from service import calculate_deadline
from schemas import RequestModel
from starlette.responses import JSONResponse

app = FastAPI()

logger.remove()
logger.add(sys.stderr, level="DEBUG")


@app.post("/")
async def main(request_json: RequestModel):
    result = calculate_deadline(request=request_json)
    return JSONResponse(status_code=status.HTTP_200_OK, content=result.json())



