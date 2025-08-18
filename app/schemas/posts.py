from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

class PostListItem(BaseModel):
    id: str = Field(..., alias="id")
    qiita_id: str
    title: str
    author: str
    template_id: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(populate_by_name=True)