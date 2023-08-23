from typing import Annotated

from fastapi import Path
from fastapi import Query
from fastapi import Depends
from fastapi import APIRouter
from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from routers.api.deps import get_async_session

from modules.database.orm.quiz import get_one
from modules.database.orm.quiz import get_topics
from modules.database.orm.quiz import get_answer
from modules.database.orm.quiz import search_quiz
from modules.database.orm.quiz import get_by_topic
from modules.database.orm.quiz import get_question

from modules.schemas.base import DetailInfo
from modules.schemas.quiz import QuizDetail
from modules.schemas.quiz import QuizAllDetail
from modules.schemas.quiz import QuizAnswerView
from modules.schemas.quiz import QuizTopicsDetail
from modules.schemas.quiz import QuizSearchDetail
from modules.schemas.quiz import QuizAnswerDetail
from modules.schemas.quiz import QuizQuestionDetail

router = APIRouter()

Session = Annotated[AsyncSession, Depends(get_async_session)]
QueryId = Annotated[int, Query(ge=1, le=2147483647)]
PathId = Annotated[int, Path(ge=1, le=2147483647)]


@router.get("/topic/all", response_model=list[QuizTopicsDetail])
async def get_all_topic(
    session: Session,
    limit: Annotated[int, Query(ge=1, le=5)] = 5,
    count_content: Annotated[int, Query(ge=1, le=5)] = 3,
    continue_after: Annotated[int, Query(ge=1, le=100)] | None = None,
):
    """Получение полного списка доступных топиков для квизов.

    Также включает небольшой список последних квизов.
    """
    result = await get_topics(session, limit, count_content, continue_after)
    return result


@router.get("/topic", response_model=list[QuizAllDetail])
async def get_topic_quiz(
    session: Session,
    topic_id: QueryId | None = None,
    limit: Annotated[int, Query(ge=1, le=20)] = 20,
    continue_after: Annotated[int, Query(ge=1, le=1000)] | None = None,
):
    """
    Если указан топик, то  происходит получение полного списка
    доступных квизов в текущем топике.

    Если топик не указан, получаем полный список доступных квизов.
    """
    result = await get_by_topic(session, topic_id, limit, continue_after)
    return result


@router.get(
    "/",
    response_model=QuizDetail,
    responses={404: {"model": DetailInfo}}
)  # fmt: skip
async def get_quiz(session: Session, quiz_id: QueryId):
    """
    Получение подробной информации по тесте.
    Также включает вопросы и описание.
    """
    result = await get_one(session, quiz_id)
    if result is None:
        raise HTTPException(404, "По Вашему запросу ничего не найдено..")
    return result


@router.post(
    "/search",
    response_model=list[QuizAllDetail],
    responses={
        400: {"model": DetailInfo},
        404: {"model": DetailInfo}
    }
)  # fmt: skip
async def search_quizzez(session: Session, schema: QuizSearchDetail):
    """Поиск квизов в топике.

    Параметры query и tags опциональны, но не могут быть оба пустыми.
    """
    if not schema.q and not schema.tags:
        raise HTTPException(400, "Одно из обязательных полей пустое..")

    result = await search_quiz(
        session,
        schema.topic_id,
        schema.q,
        schema.tags,
        schema.limit,
        schema.continue_after,
    )
    if result is None:
        raise HTTPException(404, "По Вашему запросу ничего не найдено..")
    return result


@router.get(
    "/question",
    response_model=QuizQuestionDetail,
    responses={404: {"model": DetailInfo}},
)
async def get_quiz_question(session: Session, quiz_id: QueryId, question_id: QueryId):
    """
    Получение вариантов ответа для конкретного вопроса теста.
    Также содержит подсказки.
    """
    result = await get_question(session, quiz_id, question_id)
    if result is None:
        raise HTTPException(404, "По Вашему запросу ничего не найдено..")
    return result


@router.post(
    "/answer/view",
    response_model=QuizAnswerDetail,
    responses={404: {"model": DetailInfo}},
)
async def get_quiz_answer(session: Session, schema: QuizAnswerView):
    """
    Получение ответа/ов для конкретного вопроса теста.
    Содержит информацию о правильных ответах и объяснении.
    """
    result = await get_answer(session, schema.quiz_id, schema.question_id)
    if result is None:
        raise HTTPException(404, "По Вашему запросу ничего не найдено..")
    return result
