from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str
    DEBUG: bool
    USE_DYNAMODB: bool

    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_SECONDS: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    DYNAMODB_ENDPOINT: str
    AWS_REGION: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    ADMIN_TABLE_NAME: str

    BITLY_ACCESS_TOKEN: str

    DEV_ADMIN_ID: str
    DEV_ADMIN_EMAIL: str
    DEV_ADMIN_PASSWORD: str
    DEV_ADMIN_NAME: str

    class Config:
        env_file = ".env"


settings = Settings()
