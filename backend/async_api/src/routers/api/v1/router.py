from fastapi import APIRouter

from .endpoints.auth import router as auth_router
from .endpoints.tags import router as tags_router
from .endpoints.quiz import router as quiz_router
from .endpoints.utils import router as utils_router
from .endpoints.article import router as posts_router
from .endpoints.project import router as project_router
from .endpoints.account import router as account_router
from .endpoints.hanbook import router as handbook_router

router = APIRouter(prefix="/v1")

router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(account_router, prefix="/account", tags=["account"])
router.include_router(tags_router, prefix="/tags", tags=["tags"])
router.include_router(project_router, prefix="/project", tags=["project information"])
router.include_router(posts_router, prefix="/article", tags=["article"])
router.include_router(handbook_router, prefix="/handbook", tags=["handbook"])
router.include_router(quiz_router, prefix="/quiz", tags=["quiz"])
router.include_router(utils_router, prefix="/utils", tags=["utils"])
