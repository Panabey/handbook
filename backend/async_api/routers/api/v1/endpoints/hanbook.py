from fastapi import APIRouter

router = APIRouter()


@router.get("/all")
async def get_all_handbook():
    pass


@router.get("/content")
async def get_content_handbook():
    pass


@router.get("/")
async def get_page_handbook():
    pass
