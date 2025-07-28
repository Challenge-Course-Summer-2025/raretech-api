from pydantic import BaseModel
from datetime import datetime


class TemplateItem(BaseModel):
    template_id: str
    template: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
