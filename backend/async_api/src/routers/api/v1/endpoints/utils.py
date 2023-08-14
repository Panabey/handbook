from fastapi import APIRouter

router = APIRouter()


@router.head("/healthcheck")
async def get_healthcheck():
    """Не для клиентской части.
    Используется для проверки работоспособности сервиса
    """
    pass
