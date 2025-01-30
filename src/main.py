import sys

from fastapi import FastAPI
from loguru import logger

from src.auth.router import router as auth_router
from src.config import Settings
from src.docker_app.utils import run_docker
from src.mainapp.router import router as main_router

settings = Settings.get_settings()

run_docker(
    path=settings.docker.DOCKER_PATH,
    port=settings.docker.DOCKER_PORT,
)

app = FastAPI()
app.include_router(auth_router)
app.include_router(main_router)

logger.remove()
logger.add(sys.stderr, level=settings.app.LOG_LEVEL)
