from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings

from src.db.config import DBSettings
from src.mainapp.config import APPSettings


class Settings(BaseSettings):
    db: DBSettings = Field(default_factory=DBSettings)
    app: APPSettings = Field(default_factory=APPSettings)

    @classmethod
    @lru_cache
    def get_settings(cls):
        return cls()
