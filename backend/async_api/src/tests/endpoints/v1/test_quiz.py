import pytest

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.utils.orm import insert_value
from modules.database.models import QuizTopic, Quiz, Question, Answer

pytestmark = pytest.mark.asyncio


async def test_empty_quiz(client: AsyncClient):
    """Тестирование получения конкретного квиза по id, если тот
    НЕ существует в базе данных
    """
    payload = {"quiz_id": 1}
    response = await client.get(url="/api/v1/quiz", params=payload)
    assert response.status_code == 404


async def test_quiz(client: AsyncClient, session: AsyncSession):
    """Тестирование получения конкретного квиза по id, если тот
    существует в базе данных
    """
    # Добавление топика
    data = {"title": "test_topic"}
    topic = await insert_value(QuizTopic, session, None, **data)

    # Добавление квиза
    data = {
        "topic_id": topic.id,
        "title": "test",
        "short_description": "test",
        "description": "test",
        "is_visible": True,
    }
    quiz = await insert_value(Quiz, session, None, **data)

    payload = {"quiz_id": quiz.id}
    response = await client.get(url="/api/v1/quiz", params=payload)
    assert response.status_code == 200
    assert response.json() == {
        "id": quiz.id,
        "logo_url": quiz.logo_url,
        "title": quiz.title,
        "short_description": quiz.short_description,
        "description": quiz.description,
        "questions": [],
        "topic": {"id": topic.id, "title": topic.title},
    }


async def test_empty_all_topic(client: AsyncClient):
    """Тестирование получения всех квизов в топиках, если те
    НЕ существуют в базе данных
    """
    response = await client.get("/api/v1/quiz/topic/all")
    assert response.status_code == 200
    assert response.json() == []


async def test_all_topic(client: AsyncClient, session: AsyncSession):
    """Тестирование получения всех квизов в топиках, если те
    существуют в базе данных
    """
    # Добавление топика
    data = {"title": "test_topic"}
    topic = await insert_value(QuizTopic, session, None, **data)

    response = await client.get("/api/v1/quiz/topic/all")
    # нельзя отображать пустые топики
    assert response.status_code == 200
    assert response.json() == []

    # Добавление квиза
    data = {
        "topic_id": topic.id,
        "title": "test",
        "short_description": "test",
        "description": "test",
        "is_visible": True,
    }
    quiz = await insert_value(Quiz, session, None, **data)

    response = await client.get("/api/v1/quiz/topic/all")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": topic.id,
            "title": topic.title,
            "quizzes": [
                {
                    "id": quiz.id,
                    "logo_url": quiz.logo_url,
                    "title": quiz.title,
                    "short_description": quiz.short_description,
                }
            ],
        }
    ]


async def test_empty_quiz_question(client: AsyncClient):
    """Тестирование получения списка вопросов для конкретного квиза,
    если тот НЕ существует в базе данных
    """
    data = {"quiz_id": 1, "question_id": 1}
    response = await client.get("/api/v1/quiz/question", params=data)
    assert response.status_code == 404


async def test_quiz_question(client: AsyncClient, session: AsyncSession):
    """Тестирование получения списка вопросов для конкретного квиза,
    если тот существует в базе данных
    """
    # Добавление квиза
    data = {
        "title": "test",
        "short_description": "test",
        "description": "test",
        "is_visible": True,
    }
    quiz = await insert_value(Quiz, session, None, **data)

    # Добавление вопроса для квиза
    data = {"quiz_id": quiz.id, "text": "test"}
    question = await insert_value(Question, session, None, **data)

    data = {"quiz_id": quiz.id, "question_id": question.id}
    response = await client.get("/api/v1/quiz/question", params=data)
    assert response.status_code == 200
    assert response.json() == {
        "id": question.id,
        "text": question.text,
        "hint": question.hint,
        "answers": [],
    }


async def test_empty_quiz_answer(client: AsyncClient):
    """Тестирование получения списка ответов для конкретного квиза
    по id, если тот НЕ существует в базе данных
    """
    data = {"quiz_id": 1, "question_id": 1}
    response = await client.post("/api/v1/quiz/answer/view", json=data)
    assert response.status_code == 404


async def test_quiz_answer(client: AsyncClient, session: AsyncSession):
    """Тестирование получения списка ответов для конкретного квиза
    по id, если тот существует в базе данных
    """
    # Добавление квиза
    data = {"title": "test", "short_description": "test", "description": "test"}
    quiz = await insert_value(Quiz, session, None, **data)

    # Добавление вопроса для квиза
    data = {"quiz_id": quiz.id, "text": "test"}
    question = await insert_value(Question, session, None, **data)

    # Добавление ответа на вопрос квиза
    data = {"question_id": question.id, "text": "test", "is_correct": True}
    answer = await insert_value(Answer, session, None, **data)

    data = {"quiz_id": quiz.id, "question_id": question.id}
    response = await client.post("/api/v1/quiz/answer/view", json=data)
    assert response.status_code == 200
    assert response.json() == {
        "id": question.id,
        "answers": [
            {
                "id": answer.id,
                "text": answer.text,
                "is_correct": answer.is_correct,
                "explanation": answer.explanation,
            }
        ],
    }
