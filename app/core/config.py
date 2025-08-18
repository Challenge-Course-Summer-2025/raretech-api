from typing import Optional
from pydantic_settings import BaseSettings


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
    COGNITO_APP_CLIENT_ID: Optional[str] = None

    # DynamoDB 接続
    USE_DYNAMODB: bool = True
    AWS_REGION: str
    DYNAMODB_ENDPOINT: Optional[str] = None
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None

    # DynamoDB テーブル名
    ADMINS_TABLE_NAME: str = "Admins"
    SETTINGS_TABLE_NAME: str = "Settings"
    TEMPLATES_TABLE_NAME: str = "Templates"
    POSTS_TABLE_NAME: str = "Posts"
    ARTICLE_LINK_CLICKS_TABLE_NAME: str = "Article_link_clicks"
    STATIC_LINK_CLICKS_TABLE_NAME: str = "Static_link_clicks"
    API_STATUS_TABLE_NAME: str = "API_status"

    # Short.io
    SHORTIO_API_KEY: Optional[str] = None
    SHORTIO_DOMAIN: Optional[str] = None

    class Config:
        env_file = ".env"


settings = Settings()