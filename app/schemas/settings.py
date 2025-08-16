from typing import List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class SettingsResponse(BaseModel):
    settings_id: str = Field(..., alias="id")
    ab_test_ratio: Dict[str, int] 

    model_config = ConfigDict(populate_by_name=True)


class UpdateSettingsRequest(BaseModel):
    ab_test_ratio: Dict[str, int]
