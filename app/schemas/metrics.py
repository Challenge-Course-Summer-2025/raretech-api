from pydantic import BaseModel


class MetricsResponse(BaseModel):
    total_clicks: int
    trial_class_clicks: int
    counseling_clicks: int
    ctr_average: float
    cvr_average: float
