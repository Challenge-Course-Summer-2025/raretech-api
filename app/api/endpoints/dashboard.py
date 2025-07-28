from fastapi import APIRouter, Depends
from core import security
from services.dashboard import get_dashboard_data

router = APIRouter()


@router.get("/dashboard")
async def dashboard(_: dict = Depends(security.verify_admin)):
    return await get_dashboard_data()
