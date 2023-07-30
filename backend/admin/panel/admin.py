from django.contrib import admin

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
    # A handy constant for the name of the alternate database.
    using = "handbook"

    def save_model(self, request, obj, form, change):
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        obj.delete(using=self.using)

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


class MultiModelTabularInline(admin.TabularInline):
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


admin.site.register(Quiz, MultiplyModelAdmin)
admin.site.register(QuizQuestion, QuestionAdmin)
admin.site.register(QuizAnswer, MultiplyModelAdmin)

admin.site.register(Posts, MultiplyModelAdmin)
admin.site.register(Handbook, MultiplyModelAdmin)
admin.site.register(HandbookPage, MultiplyModelAdmin)
admin.site.register(HandbookContent, MultiplyModelAdmin)
