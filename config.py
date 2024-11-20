from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    LOG_LEVEL: str
    SECRET_KEY: str
    ALGORITHM: str
    DB_TYPE: str = 'postgresql'
    DB_URL: str = '127.0.0.1'
    DB_PORT: str = '5432'
    DB_NAME: str
    DB_USER: str = 'postgres'
    DB_PASS: str = ''

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
