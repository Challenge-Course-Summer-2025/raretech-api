from fastapi import APIRouter, Depends
from core.security_cognito import verify_admin as verify_admin_dep
from services.dashboard import get_dashboard_data

router = APIRouter()

@router.get("/dashboard")
async def dashboard(_: dict = Depends(verify_admin_dep)):
    return await get_dashboard_data()
