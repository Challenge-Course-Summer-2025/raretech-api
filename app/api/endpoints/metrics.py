from fastapi import APIRouter, Depends
from core.security_cognito import verify_admin as verify_admin_dep
from services.metrics import get_metrics

router = APIRouter()

@router.get("/metrics")
async def fetch_metrics(_: dict = Depends(verify_admin_dep)):
    return await get_metrics()
