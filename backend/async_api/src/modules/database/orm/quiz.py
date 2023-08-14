from sqlalchemy import select, func
from sqlalchemy.orm import load_only, joinedload, contains_eager, defer
from sqlalchemy.ext.asyncio import AsyncSession

from modules.database.models import Quiz, Question, Answer, QuizTopic


async def get_topics(
    session: AsyncSession, limit: int, count_content: int, continue_after: int
):
    subquery = (
        select(
            QuizTopic.id,
            Quiz.id.label("quiz_id"),
            func.row_number()
            .over(partition_by=QuizTopic.id, order_by=Quiz.id.desc())
            .label("row_num"),
        )
        .join(Quiz, Quiz.topic_id == QuizTopic.id)
        .subquery()
    )

    smt = (
        select(QuizTopic)
        .join(QuizTopic.quizzes_info)
        .join(subquery, subquery.c.quiz_id == Quiz.id)
        .where(subquery.c.row_num <= count_content)
        .order_by(QuizTopic.id)
        .offset(continue_after)
        .limit(limit)
        .options(
            load_only(QuizTopic.id, QuizTopic.title),
            contains_eager(QuizTopic.quizzes_info).load_only(
                Quiz.id, Quiz.logo_url, Quiz.title, Quiz.meta
            ),
        )
    )
    result = await session.scalars(smt)
    return result.unique().all()


async def get_all(session: AsyncSession):
    smt = select(Quiz).options(defer(Quiz.description))
    result = await session.scalars(smt)
    return result.all()


async def get_one(session: AsyncSession, quiz_id: int):
    smt = (
        select(Quiz)
        .where(Quiz.id == quiz_id)
        .options(joinedload(Quiz.questions_info).load_only(Question.id))
    )
    result = await session.scalars(smt)
    return result.first()


async def get_question(session: AsyncSession, quiz_id: int, question_id: int):
    smt = (
        select(Question)
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
