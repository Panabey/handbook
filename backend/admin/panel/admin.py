from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest

from .models import (
    Quiz,
    Posts,
    Handbook,
    QuizAnswer,
    QuizQuestion,
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


class QuestionAdmin(MultiplyModelAdmin):
    inlines = [AnswerInline]


class PostAdmin(MultiplyModelAdmin):
    list_display = ("title", "create_date", "update_date")
    list_filter = ("create_date", "update_date")
    ordering = ("create_date", "update_date")
    search_fields = ("title",)
    list_per_page = 25


class HandbookAdmin(MultiplyModelAdmin):
    list_display = ("title", "is_visible")
    search_fields = ("title",)
    list_per_page = 25


class ExtendedHandbookAdmin(MultiplyModelAdmin):
    list_display = ("title", "is_visible", "create_date", "update_date")
    list_filter = ("is_visible", "create_date", "update_date")
    ordering = ("create_date", "update_date")
    search_fields = ("title",)
    list_per_page = 25


admin.site.register(Quiz, MultiplyModelAdmin)
admin.site.register(QuizQuestion, QuestionAdmin)
admin.site.register(QuizAnswer, MultiplyModelAdmin)

admin.site.register(Posts, PostAdmin)
admin.site.register(Handbook, HandbookAdmin)
admin.site.register(HandbookPage, ExtendedHandbookAdmin)
admin.site.register(HandbookContent, HandbookAdmin)
