from pydantic import Extra
from pydantic_settings import BaseSettings


class Config(BaseSettings, extra=Extra.ignore):
    class Config:
        env_file = "./.env"
        env_file_encoding = "utf-8"


class APPSettings(Config):
    LOG_LEVEL: str
    SECRET_KEY: str
    ALGORITHM: str
