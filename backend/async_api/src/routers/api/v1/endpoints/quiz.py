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
from modules.schemas.quiz import QuizInTopicDetail
from modules.schemas.quiz import QuizQuestionDetail

router = APIRouter()

Session = Annotated[AsyncSession, Depends(get_async_session)]
QueryId = Annotated[int, Query(ge=1, le=2147483647)]
PathId = Annotated[int, Path(ge=1, le=2147483647)]


@router.get(
    "/topic/all",
    response_model=list[QuizTopicsDetail],
    summary="Получение списка топиков и их квизов"
)  # fmt: skip
async def get_all_topic(
    session: Session,
    limit: Annotated[int, Query(ge=1, le=5)] = 5,
    count_content: Annotated[int, Query(ge=1, le=5)] = 3,
    continue_after: Annotated[int, Query(ge=1, le=100)] | None = None,
):
    """
    **Параметры:**\n
    `limit` - Ограничение записей топиков в ответе\n
    `count_content` - Количество записей отображаемых в каждом топике\n
    `continue_after` - Числовой идентифкикатор для продолжения с конкретной записи
    """
    result = await get_topics(session, limit, count_content, continue_after)
    return result


@router.get(
    "/topic",
    response_model=QuizInTopicDetail,
    summary="Получение списка квизов по топику",
    responses={404: {"model": DetailInfo}}
)  # fmt: skip
async def get_topic_quiz(
    session: Session,
    topic_id: QueryId | None = None,
    limit: Annotated[int, Query(ge=1, le=20)] = 20,
    continue_after: Annotated[int, Query(ge=1, le=1000)] | None = None,
):
    """
    **Параметры:**\n
    `topic_id` - Уникальный идентификатор топика (Если не указано, выведет все квизы)\n
    `limit` - Ограничение записией квизов в ответе\n
    `continue_after` - Числовой идентифкикатор для продолжения с конкретной записи
    """
    result = await get_by_topic(session, topic_id, limit, continue_after)
    if result is None:
        raise HTTPException(404, "По Вашему запросу ничего не найдено..")
    return result


@router.get(
    "",
    response_model=QuizDetail,
    summary="Получение квиза",
    responses={404: {"model": DetailInfo}}
)  # fmt: skip
async def get_quiz(session: Session, quiz_id: QueryId):
    """
    **Параметры:**\n
    `quiz_id` - Уникальный идентификатор квиза
    """
    result = await get_one(session, quiz_id)
    if result is None:
        raise HTTPException(404, "По Вашему запросу ничего не найдено..")
    return result


@router.post(
    "/search",
    response_model=list[QuizAllDetail],
    summary="Поиск по квизам",
    responses={
        400: {"model": DetailInfo},
        404: {"model": DetailInfo}
    }
)  # fmt: skip
async def search_quizzez(session: Session, schema: QuizSearchDetail):
    """
    **Параметры:**\n
    `q` - Текст для поиска по названию квиза (Не зависит от регистра)\n
    `limit` - Ограничение количества записей в ответе\n
    `tags` - Уникальные числовые идентификаторы тегов\n
    `continue_after` - Числовой идентифкикатор для продолжения с конкретной записи

    **Примечание:**\n
    Поиск осуществляется по одному или нескольким доступным параметрам: `q` и/или `tags`
    """
    if not schema.q and not schema.tags:
        raise HTTPException(400, "Одно из обязательных полей пустое..")

    result = await search_quiz(
        session,
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
    summary="Получение информации вопроса квиза",
    responses={404: {"model": DetailInfo}},
)  # fmt: skip
async def get_quiz_question(session: Session, quiz_id: QueryId, question_id: QueryId):
    """
    **Параметры:**\n
    `quiz_id` - уникальный идентификатор квиза\n
    `question_id` - уникальный идентификатор вопроса, которому принадлежит квиз

    **Примечание:**\n
    Список вопросов должен быть получен при запросе информации о квизе
    """
    result = await get_question(session, quiz_id, question_id)
    if result is None:
        raise HTTPException(404, "По Вашему запросу ничего не найдено..")
    return result


@router.post(
    "/answer/view",
    response_model=QuizAnswerDetail,
    summary="Получение ответа(ов) по вопросу",
    responses={404: {"model": DetailInfo}},
)  # fmt: skip
async def get_quiz_answer(session: Session, schema: QuizAnswerView):
    """
    **Параметры:**\n
    `quiz_id` - уникальный идентификатор квиза\n
    `question_id` - уникальный идентификатор вопроса, который принадлежит квизу
    """
    result = await get_answer(session, schema.quiz_id, schema.question_id)
    if result is None:
        raise HTTPException(404, "По Вашему запросу ничего не найдено..")
    return result
