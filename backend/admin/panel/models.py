# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to
#       the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create,
#       modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

from slugify import slugify
from mdeditor.fields import MDTextField
from .ext.utils_admin import calculate_reading_time


class Handbook(models.Model):
    title = models.CharField(max_length=80, verbose_name="Название справочника")
    description = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Описание"
    )
    is_visible = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title

    class Meta:
        managed = True
        verbose_name = "Справочник"
        verbose_name_plural = "Справочники"
        db_table = "handbook"


class HandbookContent(models.Model):
    handbook = models.ForeignKey(Handbook, models.DO_NOTHING, verbose_name="Справочник")
    title = models.CharField(max_length=80, verbose_name="Раздел справочника")
    is_visible = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title

    class Meta:
        managed = True
        verbose_name = "Раздел справочника"
        verbose_name_plural = "Разделы справочника"
        db_table = "handbook_content"


class HandbookPage(models.Model):
    handbook_title = models.ForeignKey(
        HandbookContent, models.DO_NOTHING, verbose_name="Раздел"
    )
    title = models.CharField(max_length=80, verbose_name="Название темы")
    slug = models.CharField(max_length=150, blank=True)
    text = MDTextField(verbose_name="Текст")
    reading_time = models.IntegerField(default=0, editable=False)
    update_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)
    is_visible = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        # SEO optimization
        self.slug = slugify(self.title)

        self.reading_time = calculate_reading_time(self.text)
        super().save(*args, **kwargs)

    class Meta:
        managed = True
        verbose_name = "Тема справочника"
        verbose_name_plural = "Темы справочника"
        db_table = "handbook_page"


class Posts(models.Model):
    title = models.CharField(max_length=80, verbose_name="Название поста")
    text = MDTextField(verbose_name="Текст")
    reading_time = models.IntegerField(default=0, editable=False)
    update_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        self.reading_time = calculate_reading_time(self.text)
        super().save(*args, **kwargs)

    class Meta:
        managed = True
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        db_table = "posts"


class Quiz(models.Model):
    title = models.CharField(verbose_name="Название", max_length=100)
    description = models.TextField(verbose_name="Описание", blank=True, null=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        managed = True
        db_table = "quiz"
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"


class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, models.CASCADE, verbose_name="Тест")
    title = MDTextField(verbose_name="Вопрос")
    hint = models.CharField(
        verbose_name="Подсказка", max_length=200, blank=True, null=True
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        managed = True
        db_table = "quiz_question"
        verbose_name = "Вопрос к тесту"
        verbose_name_plural = "Вопросы к тесту"


class QuizAnswer(models.Model):
    question = models.ForeignKey(QuizQuestion, models.CASCADE)
    title = models.CharField(verbose_name="Ответ", max_length=100)
    is_correct = models.BooleanField(verbose_name="Правильный?", default=False)
    explanation = models.TextField(
        verbose_name="Объсянение", max_length=200, blank=True, null=True
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        managed = True
        db_table = "quiz_answer"
        verbose_name = "Ответ к тесту"
        verbose_name_plural = "Ответы к тесту"
