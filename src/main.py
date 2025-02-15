import sys

from fastapi import FastAPI
from loguru import logger

from src.mainapp.config import SETTINGS
from src.mainapp.router import router as main_router

app = FastAPI()
app.include_router(main_router)

logger.remove()

logger.add(sys.stderr, level=SETTINGS.LOG_LEVEL)
