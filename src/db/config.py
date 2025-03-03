from pydantic import Extra
from pydantic_settings import BaseSettings


class Config(BaseSettings, extra=Extra.ignore):
    class Config:
        env_file = "./.env"
        env_file_encoding = "utf-8"


class DBSettings(Config):
    DB_TYPE: str = "postgresql+asyncpg"
    DB_ADDRESS: str = "127.0.0.1"
    DB_PORT: str = "5432"
    DB_NAME: str
    DB_USER: str = "postgres"
    DB_PASS: str = ""

    @property
    def DB_URL(self):
        url = (
            f"{self.DB_TYPE}://{self.DB_USER}"
            f"{':'+self.DB_PASS if self.DB_PASS else self.DB_PASS}"
            f"@{self.DB_ADDRESS}:{self.DB_PORT}/"
            f"{self.DB_NAME}"
        )
        return url
