from fastapi import APIRouter, Query, Depends
from core.security_cognito import verify_admin as verify_admin_dep
from services.posts import get_posts

router = APIRouter()

@router.get("/posts")
async def fetch_posts(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str | None = Query(None),
    _: dict = Depends(verify_admin_dep),
):
    return await get_posts(page=page, limit=limit, search=search)
