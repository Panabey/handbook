from sqlalchemy import func
from sqlalchemy import and_
from sqlalchemy import select
from sqlalchemy.orm import defer
from sqlalchemy.orm import load_only
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import contains_eager
from sqlalchemy.ext.asyncio import AsyncSession

from modules.database.models import Tag
from modules.database.models import Quiz
from modules.database.models import Answer
from modules.database.models import Question
from modules.database.models import QuizTopic


async def get_topics(
    session: AsyncSession, limit: int, count_content: int, continue_after: int | None
):
    subquery = (
        select(
            Quiz.topic_id,
            Quiz.id.label("quiz_id"),
            func.row_number()
            .over(partition_by=Quiz.topic_id, order_by=Quiz.id.desc())
            .label("row_num"),
        )
        .where(Quiz.is_visible)
        .subquery()
    )

    smt = (
        select(QuizTopic)
        .join(QuizTopic.quizzes_info)
        .join(
            subquery,
            and_(subquery.c.topic_id == Quiz.topic_id, subquery.c.quiz_id == Quiz.id),
        )
        .where(subquery.c.row_num <= count_content)
        .order_by(QuizTopic.id)
        .options(
            load_only(QuizTopic.id, QuizTopic.title),
            contains_eager(QuizTopic.quizzes_info).load_only(
                Quiz.id, Quiz.logo_url, Quiz.title, Quiz.short_description
            ),
        )
        .limit(limit)
        .offset(continue_after)
    )
    result = await session.scalars(smt)
    return result.unique().all()


async def get_by_topic(
    session: AsyncSession, topic_id: int, limit: int, continue_after: int | None
):
    if topic_id:
        smt = (
            select(QuizTopic)
            .join(QuizTopic.quizzes_info)
            .where(QuizTopic.id == topic_id, Quiz.is_visible)
            .order_by(Quiz.id.desc())
            .offset(continue_after)
            .limit(limit)
            .options(
                contains_eager(QuizTopic.quizzes_info)
                .defer(Quiz.description)
                .defer(Quiz.topic_id)
                .defer(Quiz.is_visible)
                .joinedload(Quiz.tags_quiz_info)
                .defer(Tag.status_id),
            )
        )
        result = await session.scalars(smt)
        return result.first()

    smt = (
        select(Quiz)
        .where(Quiz.is_visible)
        .order_by(Quiz.id.desc())
        .offset(continue_after)
        .limit(limit)
        .options(
            defer(Quiz.description),
            defer(Quiz.topic_id),
            defer(Quiz.is_visible),
            joinedload(Quiz.tags_quiz_info).defer(Tag.status_id),
        )
    )

    result = await session.scalars(smt)
    if result:
        return {"id": None, "title": None, "quizzes_info": result.unique().all()}
    return None


async def get_one(session: AsyncSession, quiz_id: int):
    smt = (
        select(Quiz)
        .join(Quiz.topic_info, isouter=True)
        .where(Quiz.id == quiz_id, Quiz.is_visible)
        .options(
            defer(Quiz.is_visible),
            joinedload(Quiz.questions_info).load_only(Question.id),
            contains_eager(Quiz.topic_info).load_only(QuizTopic.id, QuizTopic.title),
        )
    )
    result = await session.scalars(smt)
    return result.first()


async def search_quiz(
    session: AsyncSession,
    query: str | None,
    tags_id: list[int],
    limit: int,
    continue_after: int,
):
    subquery = (
        select(Quiz.id)
        .where(Quiz.is_visible)
        .order_by(Quiz.id)
        .limit(limit)
        .offset(continue_after)
    )

    if query:
        subquery = subquery.where(Quiz.title.ilike(f"%{query}%"))
    subquery = subquery.subquery()

    smt = (
        select(Quiz)
        .join(subquery, Quiz.id == subquery.c.id)
        .join(Quiz.tags_quiz_info, isouter=True)
        .order_by(Quiz.id)
        .options(
            defer(Quiz.description),
            defer(Quiz.topic_id),
            defer(Quiz.is_visible),
            contains_eager(Quiz.tags_quiz_info).defer(Tag.status_id),
        )
    )
    if tags_id:
        smt = smt.where(Tag.id.in_(tags_id))

    result = await session.scalars(smt)
    return result.unique().all()


async def get_question(session: AsyncSession, quiz_id: int, question_id: int):
    smt = (
        select(Question)
        .where(Question.quiz_id == quiz_id, Question.id == question_id)
        .options(
            load_only(Question.id, Question.text, Question.hint),
            joinedload(Question.answers_info).load_only(Answer.id, Answer.text),
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
                Answer.id, Answer.text, Answer.is_correct, Answer.explanation
            ),
        )
    )
    result = await session.scalars(smt)
    return result.first()
