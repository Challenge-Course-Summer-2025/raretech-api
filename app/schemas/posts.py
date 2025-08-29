from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

class PostListItem(BaseModel):
    id: str
    qiita_id: str
    title: str
    author: str
    template_id: Optional[str] = None
    created_at: str
    clicks_article: int = 0  # クリック数フィールドを追加
    
    model_config = ConfigDict(populate_by_name=True)