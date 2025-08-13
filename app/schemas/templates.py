from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TemplateItem(BaseModel):
    template_id: str
    template: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class TemplateCreate(BaseModel):
    template: str
    is_active: bool = True


class TemplateUpdate(BaseModel):
    template: Optional[str] = None
    is_active: Optional[bool] = None


class TemplateResponse(BaseModel):
    template_id: str
    template: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
