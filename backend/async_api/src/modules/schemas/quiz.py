from pydantic import Field
from pydantic import validator
from pydantic import BaseModel
from pydantic import AliasChoices
from pydantic import field_validator

from .tags import TagsDetail

"""
Данный блок представляет из себя схемы ответов на
конечные точки и не должны использоваться для валидации запросов
"""


class QuestionShortDetail(BaseModel):
    id: int


class AnswerShortDetail(BaseModel):
    id: int
    text: str


class AnswerDetail(BaseModel):
    id: int
    text: str
    is_correct: bool
    explanation: str | None


class QuizAllDetail(BaseModel):
    id: int
    logo_url: str | None
    title: str
    short_description: str
    tags: list[str] = Field(validation_alias=AliasChoices("tags", "tags_quiz_info"))

    @field_validator("tags", mode="before")
    @classmethod
    def tags_to_list(cls, v: list[TagsDetail]) -> list[str]:
        return [tag.title for tag in v]


class QuizInTopicDetail(BaseModel):
    id: int | None
    title: str | None
    quizzes: list[QuizAllDetail] = Field(
        validation_alias=AliasChoices("quizzes", "quizzes_info")
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
    quizzes: list[QuizAllShortDetail] = Field(
        validation_alias=AliasChoices("quizzes", "quizzes_info")
    )


class QuizDetail(BaseModel):
    id: int
    logo_url: str | None
    title: str
    short_description: str
    description: str
    questions: list[int] = Field(
        validation_alias=AliasChoices("questions", "questions_info")
    )
    topic: QuizTopicShortDetail | None = Field(
        validation_alias=AliasChoices("topic", "topic_info")
    )

    @field_validator("questions", mode="before")
    @classmethod
    def questions_to_list(cls, v: list[QuestionShortDetail]) -> list[int]:
        return [tag.id for tag in v]


class QuizQuestionDetail(BaseModel):
    id: int
    text: str
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
Данный блок представляет из себя схемы запросов для валидации
на конечные точки и не должны использоваться для валидации ответов
"""


class QuizAnswerView(BaseModel):
    quiz_id: int = Field(ge=1, le=2147483647)
    question_id: int = Field(ge=1, le=2147483647)


class QuizSearchDetail(BaseModel):
    q: str | None = Field(None, min_length=1, max_length=100)
    tags: list[int] = Field(max_length=4)
    limit: int = Field(20, ge=1, le=20)
    continue_after: int | None = Field(None, ge=1, le=1000)

    @validator("tags")
    @classmethod
    def validate_tags(cls, tags: list[int]):
        if not tags:
            return tags

        for value in tags:
            if not 1 <= value <= 2147483647:
                raise ValueError(
                    "значение должно быть в диапазоне между 1 и 2147483647"
                )
        return tags
