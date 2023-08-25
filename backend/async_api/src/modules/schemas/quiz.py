from pydantic import Field
from pydantic import BaseModel
from pydantic import AliasChoices

from .tags import TagsDetail

"""
Данный блок представляет из себя схемы ответов на
конечные точки и не должны использоваться для валидации запросов
"""


class QuestionShortDetail(BaseModel):
    id: int


class AnswerShortDetail(BaseModel):
    id: int
    title: str


class AnswerDetail(BaseModel):
    id: int
    title: str
    is_correct: bool
    explanation: str | None


class QuizAllDetail(BaseModel):
    id: int
    logo_url: str | None
    title: str
    short_description: str
    tags: list[TagsDetail] = Field(
        validation_alias=AliasChoices("tags", "tags_quiz_info")
    )


class QuizAllShortDetail(BaseModel):
    id: int
    logo_url: str | None
    title: str
    short_description: str


class QuizTopicShortDetail(BaseModel):
    id: int
    title: str


class QuizTopicsDetail(BaseModel):
    id: int
    title: str
    quizzes_info: list[QuizAllShortDetail]


class QuizDetail(BaseModel):
    id: int
    logo_url: str | None
    title: str
    short_description: str
    questions: list[QuestionShortDetail] = Field(
        validation_alias=AliasChoices("questions", "questions_info")
    )
    topic: QuizTopicShortDetail = Field(
        validation_alias=AliasChoices("topic", "topic_info")
    )


class QuizQuestionDetail(BaseModel):
    id: int
    title: str
    hint: str | None
    answers: list[AnswerShortDetail] = Field(
        validation_alias=AliasChoices("answer", "answers_info")
    )


class QuizAnswerDetail(BaseModel):
    id: int
    answers: list[AnswerDetail] = Field(
        validation_alias=AliasChoices("answer", "answers_info")
    )


class TagsDetail(BaseModel):
    id: int
    title: str


"""
Данный блок представляет из себя схемы запросов для валидации
на конечные точки и не должны использоваться для валидации ответов
"""


class QuizAnswerView(BaseModel):
    quiz_id: int = Field(ge=1, le=2147483647)
    question_id: int = Field(ge=1, le=2147483647)


class QuizSearchDetail(BaseModel):
    topic_id: int = Field(ge=1, le=2147483647)
    q: str | None = Field(None, min_length=1, max_length=80)
    tags: list[int] | None = Field(None, min_length=1, max_length=4)
    limit: int = Field(default=20, ge=1, le=20)
    continue_after: int | None = Field(default=None, ge=1, le=1000)
