from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings

from src.db.config import DBSettings
from src.docker_app.config import DockerSettings
from src.mainapp.config import APPSettings


class Settings(BaseSettings):
    db: DBSettings = Field(default_factory=DBSettings)
    app: APPSettings = Field(default_factory=APPSettings)
    docker: DockerSettings = Field(default_factory=DockerSettings)

    @classmethod
    @lru_cache
    def get_settings(cls):
        return cls()
