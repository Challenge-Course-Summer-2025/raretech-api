from fastapi import APIRouter, Depends
from schemas.settings import SettingsResponse, UpdateSettingsRequest
from services.settings import get_settings, update_settings
from core import security

router = APIRouter()


@router.get("/settings", response_model=SettingsResponse)
async def fetch_settings(_: dict = Depends(security.verify_admin)):
    return await get_settings()


@router.put("/settings")
async def update_settings_api(
    settings: UpdateSettingsRequest,
    _: dict = Depends(security.verify_admin),
):
    await update_settings(settings)
    return {"message": "設定が更新されました。"}
