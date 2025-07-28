from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from schemas.auth import TokenResponse, UserCreate, AdminInfoResponse
from core import security

router = APIRouter()

@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    existing_admin = await security.get_admin_by_email(user.email)
    if existing_admin:
        raise HTTPException(status_code=400, detail="すでに管理者が登録されています")
    await security.create_admin(user)
    return {"message": "管理者を登録しました。ログインしてください。"}

@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    admin = await security.authenticate_user(form_data.username, form_data.password)
    if not admin:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token, refresh_token = security.create_tokens(admin)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": security.ACCESS_TOKEN_EXPIRE_SECONDS
    }

@router.get("/me", response_model=AdminInfoResponse)
async def get_admin_info(current_admin: dict = Depends(security.verify_admin)):
    return current_admin
