from pydantic import BaseModel
from datetime import datetime


class PostItem(BaseModel):
    post_id: str
    qiita_id: str
    title: str
    author: str
    content: str
    template_id: str
    clicks_total: int
    clicks_trial_class: int
    clicks_counseling: int
    counseling_signups: int
    ctr: float
    cvr_counseling: float
    created_at: datetime
