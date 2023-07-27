from fastapi import APIRouter

from .endpoints.posts import router as posts_router
from .endpoints.hanbook import router as handbook_router

router = APIRouter(prefix="/v1")

router.include_router(posts_router, prefix="/post", tags=["posts"])
router.include_router(handbook_router, prefix="/handbook", tags=["handbook"])
