from fastapi import APIRouter
from api.endpoints import auth, dashboard, posts, settings, templates, metrics

router = APIRouter()


router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
router.include_router(posts.router, prefix="/posts", tags=["Posts"])
router.include_router(settings.router, prefix="/settings", tags=["Settings"])
router.include_router(templates.router, prefix="/templates", tags=["Templates"])
router.include_router(metrics.router, prefix="/metrics", tags=["Metrics"])
