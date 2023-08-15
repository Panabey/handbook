from pydantic import Field
from pydantic import BaseModel
from pydantic import AliasChoices


"""
Данный блок представляет из себя ответы на конечные точки
и не должны использоваться для валидации запросов
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


class TagsDetail(BaseModel):
    id: int
    title: str


class QuizAllDetail(BaseModel):
    id: int
    logo_url: str | None
    title: str
    meta: str
    tags: list[TagsDetail] = Field(validation_alias=AliasChoices("tags", "tags_info"))


class QuizTopicsDetail(BaseModel):
    id: int
    title: str
    quizzes_info: list[QuizAllDetail]


class QuizDetail(QuizAllDetail):
    questions: list[QuestionShortDetail] = Field(
        validation_alias=AliasChoices("questions", "questions_info")
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


"""
Данный блок представляет из себя запросы для валидации
на конечные точки и не должны использоваться для валидации ответов
"""


class QuizAnswerView(BaseModel):
    quiz_id: int = Field(ge=1, le=2147483647)
    question_id: int = Field(ge=1, le=2147483647)
