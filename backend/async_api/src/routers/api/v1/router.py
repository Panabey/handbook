from fastapi import APIRouter

from .endpoints.quiz import router as quiz_router
from .endpoints.article import router as posts_router
from .endpoints.utils import router as utils_router
from .endpoints.hanbook import router as handbook_router

router = APIRouter(prefix="/v1")

router.include_router(posts_router, prefix="/article", tags=["article"])
router.include_router(handbook_router, prefix="/handbook", tags=["handbook"])
router.include_router(quiz_router, prefix="/quiz", tags=["quiz"])
router.include_router(utils_router, prefix="/utils", tags=["utils"])
