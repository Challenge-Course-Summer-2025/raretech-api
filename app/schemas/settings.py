from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class SettingsResponse(BaseModel):
    settings_id: str = Field(..., alias="id")
    check_interval: int
    excluded_users: List[str]
    excluded_keywords: List[str]
    trial_class_link: str
    counseling_link: str
    last_checked_at: datetime

    class Config:
        allow_population_by_field_name = True


class UpdateSettingsRequest(BaseModel):
    check_interval: int
    excluded_users: List[str]
    excluded_keywords: List[str]
    trial_class_link: str
    counseling_link: str
