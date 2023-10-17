from fastapi import APIRouter

router = APIRouter()


@router.head(
    "/healthcheck",
    summary="Проверка работоспособности сервиса"
)  # fmt: skip
async def get_healthcheck():
    return None
