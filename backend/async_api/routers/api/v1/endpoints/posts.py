from fastapi import APIRouter

router = APIRouter()


@router.get("/all")
async def get_all_posts():
    pass


@router.get("/")
async def get_page_post():
    pass
