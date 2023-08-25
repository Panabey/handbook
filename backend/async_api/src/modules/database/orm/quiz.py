from sqlalchemy import func
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
    session: AsyncSession, limit: int, count_content: int, continue_after: int
):
    # отстортированный список последних добавленных тем
    subquery = select(
        Quiz.topic_id,
        Quiz.id.label("quiz_id"),
        func.row_number()
        .over(partition_by=Quiz.topic_id, order_by=Quiz.id.desc())
        .label("row_num"),
    ).subquery()

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
                Quiz.id, Quiz.logo_url, Quiz.title, Quiz.short_description
            ),
        )
    )
    result = await session.scalars(smt)
    return result.unique().all()


async def get_by_topic(
    session: AsyncSession, topic_id: int, limit: int, continue_after: int
):
    smt = (
        select(Quiz)
        .order_by(Quiz.id.desc())
        .offset(continue_after)
        .limit(limit)
        .options(
            defer(Quiz.description),
            defer(Quiz.topic_id),
            joinedload(Quiz.tags_quiz_info),
        )
    )
    if topic_id:
        smt = smt.where(Quiz.topic_id == topic_id)

    result = await session.scalars(smt)
    return result.unique().all()


async def get_one(session: AsyncSession, quiz_id: int):
    smt = (
        select(Quiz)
        .join(Quiz.topic_info, isouter=True)
        .where(Quiz.id == quiz_id)
        .options(
            joinedload(Quiz.questions_info).load_only(Question.id),
            contains_eager(Quiz.topic_info).load_only(QuizTopic.id, QuizTopic.title),
        )
    )
    result = await session.scalars(smt)
    return result.first()


async def search_quiz(
    session: AsyncSession,
    topic_id: int,
    query: str,
    tags_id: list[int],
    limit: int,
    continue_after: int,
):
    smt = (
        select(Quiz)
        .join(Quiz.tags_quiz_info, isouter=True)
        .where(Quiz.topic_id == topic_id)
        .order_by(Quiz.id.desc())
        .offset(continue_after)
        .limit(limit)
        .options(
            defer(Quiz.description),
            defer(Quiz.topic_id),
            contains_eager(Quiz.tags_quiz_info),
        )
    )

    if query:
        smt = smt.where(Quiz.title.ilike(f"%{query}%"))
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
