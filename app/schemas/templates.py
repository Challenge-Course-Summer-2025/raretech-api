from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class TemplateItem(BaseModel):
    template_id: str = Field(..., alias="id")
    template: str
    is_active: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(populate_by_name=True)


class TemplateCreate(BaseModel):
    template: str
    is_active: int = 0


class TemplateUpdate(BaseModel):
    template: Optional[str] = None
    is_active: Optional[int] = None


class TemplateResponse(BaseModel):
    template_id: str = Field(..., alias="id")
    template: str
    is_active: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(populate_by_name=True)