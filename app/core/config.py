from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App
    ENV: str = "dev"
    DEBUG: bool = True

    # Auth provider
    AUTH_PROVIDER: str = "cognito"

    # Cognito
    COGNITO_REGION: str
    COGNITO_USER_POOL_ID: str
    COGNITO_JWKS_URL: str
    COGNITO_ISSUER: str
    COGNITO_ACCEPTED_TOKEN_USE: str = "access"
    COGNITO_APP_CLIENT_ID: str | None = None

    # DynamoDB
    USE_DYNAMODB: bool = True
    ADMIN_TABLE_NAME: str = "AdminsTable"
    DYNAMODB_ENDPOINT: str | None = None
    AWS_REGION: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str

    # Short.io
    SHORTIO_API_KEY: str | None = None
    SHORTIO_DOMAIN: str | None = None

    class Config:
        env_file = ".env"


settings = Settings()