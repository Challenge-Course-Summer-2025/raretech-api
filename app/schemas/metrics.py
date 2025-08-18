from pydantic import BaseModel


class ArticleMetrics(BaseModel):
    clicks: int
    x_views: int
    ctr: float


class StaticLinkMetrics(BaseModel):
    clicks_trial_lesson: int
    clicks_counseling: int
    tweet_views: int
    ctr_trial_lesson: float
    ctr_counseling: float


class MetricsResponse(BaseModel):
    total_clicks: int
    trial_class_clicks: int
    counseling_clicks: int
    ctr_average: float
    cvr_average: float
