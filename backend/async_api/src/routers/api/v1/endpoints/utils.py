from fastapi import APIRouter

router = APIRouter()


@router.head(
    "/healthcheck",
    summary="Проверки работоспособности сервиса"
)  # fmt: skip
async def get_healthcheck():
    """Не для клиентской части.
    Используется для проверки работоспособности сервиса
    """
    return None
