from clients.dynamodb import get_settings_data, update_settings_data
from schemas.settings import SettingsResponse
from fastapi import HTTPException
from datetime import datetime

async def get_settings() -> SettingsResponse:
    try:
        settings_dict = get_settings_data()

        if not settings_dict or not isinstance(settings_dict, dict):
            return SettingsResponse(
                id="default-id",
                check_interval=60,
                excluded_users=[],
                excluded_keywords=[],
                trial_class_link="",
                counseling_link="",
                last_checked_at=datetime.utcnow(),
            )

        return SettingsResponse(**settings_dict)
    except Exception as e:
        print(f"設定データの取得に失敗しました: {e}")
        raise HTTPException(status_code=500, detail="設定データの取得に失敗しました")

async def update_settings(new_settings: dict):
    await update_settings_data(new_settings)
    return {"message": "設定を更新しました"}
