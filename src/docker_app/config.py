import os
from pydantic import Extra
from pydantic_settings import BaseSettings


class Config(BaseSettings, extra=Extra.ignore):
    class Config:
        env_file = "./.env"
        env_file_encoding = "utf-8"


class DockerSettings(Config):
    DOCKER_MODE: bool = True
    DOCKER_PATH: str = os.getcwd() + '\\src\\docker_app\\'

