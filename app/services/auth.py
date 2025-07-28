from fastapi import HTTPException, status, Request, Response
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
import os
import uuid

# === JWT設定 ===
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret") 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = int(os.getenv("ACCESS_TOKEN_EXPIRE_SECONDS", "900"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "14"))
IS_PROD = os.getenv("ENV") == "production"

# === ハッシュ化 ===
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# === モックデータ ===
MOCK_ADMIN = {}

def create_access_token(admin: dict) -> str:
    expire = datetime.utcnow() + timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS)
    payload = {
        "sub": admin["admin_id"],
        "email": admin["email"],
        "user_name": admin["user_name"],
        "exp": expire
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(admin: dict) -> str:
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {
        "sub": admin["admin_id"],
        "exp": expire
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_jwt_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="トークンが無効です"
        )

async def get_admin_by_email(email: str) -> dict | None:
    if MOCK_ADMIN.get("email") == email:
        return MOCK_ADMIN
    return None

async def create_admin(user) -> None:
    global MOCK_ADMIN
    if MOCK_ADMIN.get("email") == user.email:
        raise HTTPException(status_code=400, detail="すでに管理者が登録されています")

    now = datetime.utcnow().isoformat()
    MOCK_ADMIN = {
        "admin_id": str(uuid.uuid4()), 
        "email": user.email,
        "user_name": user.user_name,
        "hashed_password": pwd_context.hash(user.password),
        "created_at": now,
        "updated_at": now
    }

async def authenticate_user(email: str, password: str) -> dict | None:
    admin = await get_admin_by_email(email)
    if admin and pwd_context.verify(password, admin["hashed_password"]):
        return admin
    return None

def create_tokens(admin: dict) -> tuple[str, str]:
    return create_access_token(admin), create_refresh_token(admin)

def refresh_access_token(request: Request) -> str:
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=401, detail="リフレッシュトークンがありません")
    payload = decode_jwt_token(token)
    return create_access_token({
        "admin_id": payload["sub"],
        "email": MOCK_ADMIN["email"],
        "user_name": MOCK_ADMIN["user_name"]
    })

def set_refresh_cookie(response: Response, refresh_token: str):
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=IS_PROD,
        samesite="lax",
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
    )

def clear_refresh_cookie(response: Response):
    response.delete_cookie("refresh_token")

def verify_admin(token: str) -> dict:
    payload = decode_jwt_token(token)
    if not MOCK_ADMIN or payload.get("sub") != MOCK_ADMIN.get("admin_id"):
        raise HTTPException(status_code=401, detail="無効な管理者")
    return MOCK_ADMIN
