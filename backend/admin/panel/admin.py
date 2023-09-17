from typing import Any

from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest

from .models import (
    Tag,
    Quiz,
    QuizTag,
    QuizTopic,
    QuizAnswer,
    QuizQuestion,
    TagStatus,
    Article,
    ArticleTag,
    HandBookStatus,
    Handbook,
    HandbookPage,
    HandbookContent,
    ProjectNews,
)

from .forms import AnswerForm, TagsForm


class MultiplyModelAdmin(admin.ModelAdmin):
    """Расширеная модель для подключения сторонней базы данных"""

    using = "handbook"

    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        obj.save(using=self.using)

    def delete_model(self, request: HttpRequest, obj: Any) -> None:
        obj.delete(using=self.using)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return super().formfield_for_foreignkey(
            db_field, request, using=self.using, **kwargs
        )

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        return super().formfield_for_manytomany(
            db_field, request, using=self.using, **kwargs
        )


class MultiModelTabularInline(admin.TabularInline):
    """Расширеная модель для соеденения нескольхих таблиц"""

    using = "handbook"

    def get_queryset(self, request):
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return super().formfield_for_foreignkey(
            db_field, request, using=self.using, **kwargs
        )

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        return super().formfield_for_manytomany(
            db_field, request, using=self.using, **kwargs
        )


class ProjectNewsAdmin(MultiplyModelAdmin):
    list_display = ("title", "create_date")
    search_fields = ("title",)
    list_filter = ("create_date",)
    ordering = ("-create_date",)
    list_per_page = 20


class TagAdmin(MultiplyModelAdmin):
    list_display = ("title", "status")
    list_filter = ("status",)
    search_fields = ("title", "status")
    list_per_page = 20


class AnswerInline(MultiModelTabularInline):
    model = QuizAnswer
    formset = AnswerForm
    extra = 1
    min_num = 2
    max_num = 4


class QuizTagInline(MultiModelTabularInline):
    model = QuizTag
    formset = TagsForm
    extra = 1
    max_num = 3


class QuizTopicAdmin(MultiplyModelAdmin):
    search_fields = ("title",)
    ordering = ("-id",)
    list_per_page = 20


class QuizAdmin(MultiplyModelAdmin):
    inlines = [QuizTagInline]
    list_display = ("title", "topic", "is_visible")
    list_filter = ("topic", "is_visible")
    search_fields = ("title", "topic__title")
    ordering = ("-id",)
    list_per_page = 20
    autocomplete_fields = ("topic",)


class QuestionAdmin(MultiplyModelAdmin):
    inlines = [AnswerInline]
    list_display = ("question_number", "quiz")
    search_fields = ("quiz__title",)
    ordering = ("-id",)
    autocomplete_fields = ("quiz",)

    def question_number(self, obj: QuizQuestion) -> str:
        return f"Вопрос #{obj.pk}"

    question_number.short_description = "Вопрос"


class AnswerAdmin(MultiplyModelAdmin):
    list_display = ("text", "get_question", "get_quiz")
    search_fields = ("question__quiz__title",)
    ordering = ("-id",)

    def get_quiz(self, obj: QuizAnswer):
        return obj.question.quiz.title

    def get_question(self, obj: QuizAnswer):
        return f"Вопрос #{obj.question.pk}"

    get_quiz.short_description = "Квиз"
    get_question.short_description = "Вопрос"


class ArticleTagInline(MultiModelTabularInline):
    model = ArticleTag
    formset = TagsForm
    extra = 1
    max_num = 3


class ArticleAdmin(MultiplyModelAdmin):
    inlines = [ArticleTagInline]

    list_display = ("title", "create_date", "update_date")
    list_filter = ("create_date", "update_date")
    ordering = ("-create_date",)
    search_fields = ("title",)
    list_per_page = 20


class HandbookAdmin(MultiplyModelAdmin):
    list_display = ("title", "is_visible")
    search_fields = ("title",)
    list_filter = ("is_visible",)
    ordering = ("-id",)
    list_per_page = 20


class HandbookStatusAdmin(MultiplyModelAdmin):
    list_display = ("title", "color_text", "color_background")
    search_fields = ("title",)
    list_per_page = 20


class HandbookContentAdmin(MultiplyModelAdmin):
    list_display = ("handbook", "title")
    search_fields = ("title", "handbook__title")
    list_filter = ("handbook",)
    ordering = ("-id",)
    list_per_page = 20
    autocomplete_fields = ("handbook",)


class HandbookPageAdmin(MultiplyModelAdmin):
    list_display = (
        "title",
        "get_content",
        "get_handbook",
        "create_date",
        "update_date",
    )
    list_filter = ("create_date", "update_date", "content__handbook")
    ordering = ("-update_date",)
    search_fields = ("title", "content__handbook__title")
    list_per_page = 20
    autocomplete_fields = ("content",)

    def get_handbook(self, obj: HandbookPage):
        return obj.content.handbook.title

    def get_content(self, obj: HandbookPage):
        return obj.content.title

    get_handbook.short_description = "Справочник"
    get_content.short_description = "Раздел"


# Общие теги
admin.site.register(Tag, TagAdmin)
admin.site.register(TagStatus, MultiplyModelAdmin)

# Квизы
admin.site.register(Quiz, QuizAdmin)
admin.site.register(QuizTopic, QuizTopicAdmin)
admin.site.register(QuizQuestion, QuestionAdmin)
admin.site.register(QuizAnswer, AnswerAdmin)

# Статьи
admin.site.register(Article, ArticleAdmin)

# Новости проекта
admin.site.register(ProjectNews, ProjectNewsAdmin)

# Справочники
admin.site.register(HandBookStatus, HandbookStatusAdmin)
admin.site.register(Handbook, HandbookAdmin)
admin.site.register(HandbookPage, HandbookPageAdmin)
admin.site.register(HandbookContent, HandbookContentAdmin)
