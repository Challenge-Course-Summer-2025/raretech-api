from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TemplateItem(BaseModel):
    template_id: str
    template: str
    is_active: int
    created_at: datetime
    updated_at: datetime


class TemplateCreate(BaseModel):
    template: str
    is_active: int = 0


class TemplateUpdate(BaseModel):
    template: Optional[str] = None
    is_active: Optional[int] = None


class TemplateResponse(BaseModel):
    template_id: str
    template: str
    is_active: int
    created_at: datetime
    updated_at: datetime
