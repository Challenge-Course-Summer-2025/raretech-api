from fastapi import APIRouter, Query, Depends
from core import security
from services.posts import get_posts

router = APIRouter()


@router.get("/posts")
async def fetch_posts(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str = Query(None),
    _: dict = Depends(security.verify_admin),
):
    return await get_posts(page=page, limit=limit, search=search)
