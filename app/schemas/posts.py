from pydantic import BaseModel
from datetime import datetime


class PostItem(BaseModel):
    post_id: str
    qiita_id: str
    title: str
    author: str
    content: str
    template_id: str
    created_at: datetime
