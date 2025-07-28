from fastapi import APIRouter, Depends
from core import security
from services.metrics import get_metrics

router = APIRouter()


@router.get("/metrics")
async def fetch_metrics(_: dict = Depends(security.verify_admin)):
    return await get_metrics()
