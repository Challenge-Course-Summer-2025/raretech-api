from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from services import auth

# JWTを取得するためのOAuth2スキーム（Authorizationヘッダから読み取る）
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# アクセストークンの検証ロジック
async def verify_admin(token: str = Depends(oauth2_scheme)) -> dict:
    return auth.verify_admin(token)

# 以下はサービス層への委譲（そのままでOK）
get_admin_by_email = auth.get_admin_by_email
create_admin = auth.create_admin
authenticate_user = auth.authenticate_user
create_tokens = auth.create_tokens
refresh_access_token = auth.refresh_access_token
set_refresh_cookie = auth.set_refresh_cookie
clear_refresh_cookie = auth.clear_refresh_cookie
ACCESS_TOKEN_EXPIRE_SECONDS = auth.ACCESS_TOKEN_EXPIRE_SECONDS
