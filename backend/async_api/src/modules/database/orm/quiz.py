from sqlalchemy import select
from sqlalchemy.orm import load_only, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from modules.database.models import Quiz, Question, Answer


async def get_all(session: AsyncSession):
    smt = select(Quiz)
    result = await session.scalars(smt)
    return result.all()


async def get_one(session: AsyncSession, quiz_id: int):
    smt = (
        select(Quiz)
        .join(Quiz.questions_info)
        .where(Quiz.id == quiz_id)
        .options(joinedload(Quiz.questions_info).load_only(Question.id))
    )
    result = await session.scalars(smt)
    return result.first()


async def get_question(session: AsyncSession, quiz_id: int, question_id: int):
    smt = (
        select(Question)
        .join(Question.answers_info)
        .where(Question.quiz_id == quiz_id, Question.id == question_id)
        .options(
            load_only(Question.id, Question.title, Question.hint),
            joinedload(Question.answers_info).load_only(Answer.id, Answer.title),
        )
    )
    result = await session.scalars(smt)
    return result.first()


async def get_answer(session: AsyncSession, quiz_id: int, question_id: int):
    smt = (
        select(Question)
        .join(Question.answers_info)
        .where(Question.quiz_id == quiz_id, Question.id == question_id)
        .options(
            load_only(Question.id),
            joinedload(Question.answers_info).load_only(
                Answer.id, Answer.title, Answer.is_correct, Answer.explanation
            ),
        )
    )
    result = await session.scalars(smt)
    return result.first()
