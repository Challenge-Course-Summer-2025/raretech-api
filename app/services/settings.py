from clients.dynamodb import get_settings_data, update_settings_data
from schemas.settings import SettingsResponse
from fastapi import HTTPException


async def get_settings() -> SettingsResponse:
    try:
        settings_dict = get_settings_data()
        return SettingsResponse(**settings_dict)
    except Exception as e:
        print(f"設定データの取得に失敗しました: {e}")
        raise HTTPException(status_code=500, detail="設定データの取得に失敗しました")


async def update_settings(new_settings: dict):
    ok = update_settings_data(new_settings)
    if not ok:
        raise HTTPException(status_code=500, detail="設定データの更新に失敗しました")
    return {"message": "設定を更新しました"}
