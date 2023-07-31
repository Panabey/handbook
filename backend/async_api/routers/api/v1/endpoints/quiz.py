from typing import Annotated

from fastapi import Query, Path
from fastapi import Depends
from fastapi import APIRouter

from sqlalchemy.ext.asyncio import AsyncSession

from routers.api.deps import get_async_session
from modules.database.orm.quiz import get_all
from modules.database.orm.quiz import get_one
from modules.database.orm.quiz import get_question
from modules.database.orm.quiz import get_answer

from modules.schemas.quiz import QuizAllDetail
from modules.schemas.quiz import QuizDetail
from modules.schemas.quiz import QuizQuestionDetail
from modules.schemas.quiz import QuizAnswerDetail

from modules.schemas.quiz import QuizAnswerView

router = APIRouter()

Session = Annotated[AsyncSession, Depends(get_async_session)]
QueryId = Annotated[int, Query(ge=1, le=2147483647)]
PathId = Annotated[int, Path(ge=1, le=2147483647)]


@router.get("/all", response_model=list[QuizAllDetail])
async def get_all_quiz(session: Session):
    result = await get_all(session)
    return result


@router.get("/{quiz_id}", response_model=QuizDetail)
async def get_quiz(session: Session, quiz_id: PathId):
    result = await get_one(session, quiz_id)
    return result


@router.get("/{quiz_id}/question", response_model=QuizQuestionDetail)
async def get_quiz_question(session: Session, quiz_id: PathId, question_id: QueryId):
    result = await get_question(session, quiz_id, question_id)
    return result


@router.post("/answer/view", response_model=QuizAnswerDetail)
async def get_quiz_answer(session: Session, schema: QuizAnswerView):
    result = await get_answer(session, schema.quiz_id, schema.question_id)
    return result
