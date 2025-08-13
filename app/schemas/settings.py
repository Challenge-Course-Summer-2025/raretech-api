from typing import List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class SettingsResponse(BaseModel):
    settings_id: str = Field(..., alias="id")
    check_interval: int
    excluded_users: List[str]
    excluded_keywords: List[str]
    trial_class_link: str
    counseling_link: str
    last_checked_at: datetime

    model_config = ConfigDict(populate_by_name=True)


class UpdateSettingsRequest(BaseModel):
    check_interval: int
    excluded_users: List[str]
    excluded_keywords: List[str]
    trial_class_link: str
    counseling_link: str
