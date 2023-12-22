from typing import Any

from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest

from core.settings import settings

from .models import (
    Tag,
    Quiz,
    QuizTag,
    QuizTopic,
    QuizAnswer,
    QuizQuestion,
    TagStatus,
    Book,
    Article,
    ArticleTag,
    HandBookStatus,
    HandbookCategory,
    Handbook,
    HandbookPage,
    HandbookContent,
    ProjectNews,
)

from .forms import AnswerForm, TagsForm


class MultiplyModelAdmin(admin.ModelAdmin):
    """Расширеная модель для подключения сторонней базы данных"""

    using = settings.DB_BACKEND_NAME

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

    using = settings.DB_BACKEND_NAME

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
    list_filter = ("status__title",)
    search_fields = ("title", "status__title")
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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        kwargs["queryset"] = Tag.objects.filter(status__title="quiz")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class QuizTopicAdmin(MultiplyModelAdmin):
    search_fields = ("title",)
    ordering = ("-id",)
    list_per_page = 20


class QuizAdmin(MultiplyModelAdmin):
    inlines = [QuizTagInline]
    list_display = ("title", "topic", "is_visible", "questions_count")
    list_filter = ("topic", "is_visible")
    search_fields = ("title", "topic__title")
    ordering = ("-id",)
    list_per_page = 20
    autocomplete_fields = ("topic",)

    def questions_count(self, obj: Quiz):
        return obj.quizquestion_set.count()

    questions_count.short_description = "Количество вопросов"


class QuestionAdmin(MultiplyModelAdmin):
    inlines = [AnswerInline]
    list_display = ("__str__", "quiz")
    search_fields = ("quiz__title",)
    ordering = ("-id",)
    autocomplete_fields = ("quiz",)


class AnswerAdmin(MultiplyModelAdmin):
    list_display = ("__str__", "question", "get_quiz")
    search_fields = ("question__quiz__title",)
    ordering = ("-id",)

    def get_quiz(self, obj: QuizAnswer):
        return obj.question.quiz.title

    get_quiz.short_description = "Квиз"


class ArticleTagInline(MultiModelTabularInline):
    model = ArticleTag
    formset = TagsForm
    extra = 1
    max_num = 3

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        kwargs["queryset"] = Tag.objects.filter(status__title="article")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ArticleAdmin(MultiplyModelAdmin):
    inlines = [ArticleTagInline]

    list_display = ("title", "create_date", "update_date")
    list_filter = ("create_date", "update_date")
    ordering = ("-create_date",)
    search_fields = ("title",)
    list_per_page = 20


class HandbookAdmin(MultiplyModelAdmin):
    list_display = ("title", "category", "is_visible", "status")
    search_fields = ("title",)
    list_filter = ("is_visible", "status__title", "category__title")
    autocomplete_fields = ("category",)
    ordering = ("-id",)
    list_per_page = 20


class HandbookCategoryAdmin(MultiplyModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)
    ordering = ("-id",)
    list_per_page = 20


class HandbookStatusAdmin(MultiplyModelAdmin):
    list_display = ("title", "color_text", "color_background")
    search_fields = ("title",)
    list_per_page = 20


class HandbookContentAdmin(MultiplyModelAdmin):
    list_display = ("handbook", "get_full_title")
    search_fields = ("title", "handbook__title")
    list_filter = ("handbook__title",)
    ordering = ("-id",)
    list_per_page = 20
    autocomplete_fields = ("handbook",)

    def get_full_title(self, obj: HandbookContent):
        return f"{obj.part}. {obj.title}"

    get_full_title.short_description = "Название раздела"


class HandbookPageAdmin(MultiplyModelAdmin):
    list_display = (
        "get_full_title",
        "content",
        "get_handbook",
        "create_date",
        "update_date",
    )
    list_filter = ("create_date", "update_date", "content__handbook__title")
    ordering = ("-update_date",)
    search_fields = ("title", "content__handbook__title")
    list_per_page = 20
    autocomplete_fields = ("content",)

    def get_full_title(self, obj: HandbookPage):
        return f"{obj.content.part}.{obj.subpart} {obj.title}"

    def get_handbook(self, obj: HandbookPage):
        return obj.content.handbook.title

    get_full_title.short_description = "Название страницы"
    get_handbook.short_description = "Справочник"


class BookAdmin(MultiplyModelAdmin):
    list_display = ("title", "author", "handbook", "is_display")
    list_filter = ("is_display", "handbook__title")
    search_fields = ("title", "author")
    ordering = ("-id",)
    list_per_page = 20
    autocomplete_fields = ("handbook",)


class TagStatusAdmin(MultiplyModelAdmin):
    ordering = ("-id",)
    list_per_page = 20


# Общие теги
admin.site.register(Tag, TagAdmin)
admin.site.register(TagStatus, TagStatusAdmin)

# Квизы
admin.site.register(Quiz, QuizAdmin)
admin.site.register(QuizTopic, QuizTopicAdmin)
admin.site.register(QuizQuestion, QuestionAdmin)
admin.site.register(QuizAnswer, AnswerAdmin)

# Книги
admin.site.register(Book, BookAdmin)

# Статьи
admin.site.register(Article, ArticleAdmin)

# Новости проекта
admin.site.register(ProjectNews, ProjectNewsAdmin)

# Справочники
admin.site.register(HandbookCategory, HandbookCategoryAdmin)
admin.site.register(HandBookStatus, HandbookStatusAdmin)
admin.site.register(Handbook, HandbookAdmin)
admin.site.register(HandbookPage, HandbookPageAdmin)
admin.site.register(HandbookContent, HandbookContentAdmin)
