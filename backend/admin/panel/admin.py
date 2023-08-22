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
    Article,
    ArticleTag,
    Status,
    Handbook,
    HandbookPage,
    HandbookContent,
)


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


class AnswerInline(MultiModelTabularInline):
    model = QuizAnswer
    extra = 1
    min_num = 2
    max_num = 4


class QuizTagInline(MultiModelTabularInline):
    model = QuizTag
    extra = 1
    max_num = 3


class QuizTopicAdmin(MultiplyModelAdmin):
    search_fields = ("title",)
    list_per_page = 20


class QuizAdmin(MultiplyModelAdmin):
    inlines = [QuizTagInline]
    list_display = ("title", "topic")
    search_fields = ("title", "topic")
    list_per_page = 20


class QuestionAdmin(MultiplyModelAdmin):
    inlines = [AnswerInline]


class ArticleTagInline(MultiModelTabularInline):
    model = ArticleTag
    extra = 1
    max_num = 3


class ArticleAdmin(MultiplyModelAdmin):
    inlines = [ArticleTagInline]

    list_display = ("title", "create_date", "update_date")
    list_filter = ("create_date", "update_date")
    ordering = ("create_date", "update_date")
    search_fields = ("title",)
    list_per_page = 20


class HandbookAdmin(MultiplyModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)
    list_per_page = 20


class HandbookContentAdmin(MultiplyModelAdmin):
    list_display = ("handbook", "title")
    search_fields = ("title", "handbook__title")
    list_per_page = 20


class HandbookPageAdmin(MultiplyModelAdmin):
    list_display = (
        "title",
        "content",
        "get_handbook",
        "create_date",
        "update_date",
    )
    list_filter = ("create_date", "update_date")
    ordering = ("create_date", "update_date")
    search_fields = ("title", "content__handbook__title")
    list_per_page = 20

    def get_handbook(self, obj: HandbookPage):
        return obj.content.handbook.title

    get_handbook.short_description = "Справочник"


admin.site.register(Tag, MultiplyModelAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(QuizTopic, QuizTopicAdmin)
admin.site.register(QuizQuestion, QuestionAdmin)
admin.site.register(QuizAnswer, MultiplyModelAdmin)

admin.site.register(Article, ArticleAdmin)

admin.site.register(Status, MultiplyModelAdmin)
admin.site.register(Handbook, HandbookAdmin)
admin.site.register(HandbookPage, HandbookPageAdmin)
admin.site.register(HandbookContent, HandbookContentAdmin)
