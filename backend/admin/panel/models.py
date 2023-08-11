# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to
#       the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create,
#       modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
import re

from typing import Collection
from django.db import models
from django.core.exceptions import ValidationError

from mdeditor.fields import MDTextField
from .ext.utils_admin import calculate_reading_time


class Status(models.Model):
    title = models.CharField(max_length=25, verbose_name="Название статуса")

    def __str__(self) -> str:
        return self.title

    class Meta:
        managed = False
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"
        db_table = "status"


class Handbook(models.Model):
    logo_url = models.FileField(
        "Изображение", upload_to="images/handbook", blank=True, null=True
    )
    title = models.CharField("Название справочника", max_length=80)
    description = models.TextField("Описание", max_length=255, blank=True, null=True)
    is_visible = models.BooleanField("Видимый?", default=False)
    status = models.ForeignKey(
        "Status", models.SET_NULL, blank=True, null=True, verbose_name="Статус"
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        managed = False
        verbose_name = "Справочник"
        verbose_name_plural = "Справочники"
        db_table = "handbook"


class HandbookContent(models.Model):
    handbook = models.ForeignKey(Handbook, models.DO_NOTHING, verbose_name="Справочник")
    title = models.CharField(
        "Раздел справочника", help_text="Например: 1. Основы", max_length=80
    )
    is_visible = models.BooleanField("Видимый?", default=False)

    def __str__(self) -> str:
        return self.title

    def clean_fields(self, exclude: Collection[str] | None) -> None:
        errors = {}
        # шаблон <число>. <текст>
        if not re.match(r"^\d+\.\s.+", self.title):
            errors["title"] = ValidationError("Несоответствие шаблону")
        if errors:
            raise ValidationError(errors)
        return super().clean_fields(exclude)

    class Meta:
        managed = False
        verbose_name = "Раздел справочника"
        verbose_name_plural = "Разделы справочника"
        db_table = "handbook_content"


class HandbookPage(models.Model):
    content = models.ForeignKey(
        HandbookContent, models.DO_NOTHING, verbose_name="Раздел"
    )
    title = models.CharField(
        "Название темы", help_text="Например: 1.1 Циклы", max_length=80
    )
    text = MDTextField("Текст")
    reading_time = models.IntegerField(default=0, editable=False)
    update_date = models.DateTimeField("Дата создания", auto_now=True)
    create_date = models.DateTimeField("Дата редактирования", auto_now_add=True)
    is_visible = models.BooleanField("Видимый?", default=False)

    def __str__(self) -> str:
        return self.title

    def clean_fields(self, exclude: Collection[str] | None) -> None:
        errors = {}
        # шаблон <число>.<число>. <текст>
        if not re.match(r"^\d+\.\d+\s.+", self.title):
            errors["title"] = ValidationError("Несоответствие шаблону")
        if errors:
            raise ValidationError(errors)
        return super().clean_fields(exclude)

    def save(self, *args, **kwargs):
        self.reading_time = calculate_reading_time(self.text)
        super().save(*args, **kwargs)

    class Meta:
        managed = False
        verbose_name = "Тема справочника"
        verbose_name_plural = "Темы справочника"
        db_table = "handbook_page"


class Post(models.Model):
    title = models.CharField("Название поста", max_length=80)
    anons = models.TextField("Краткое содержание", max_length=255)
    text = MDTextField("Текст")
    reading_time = models.IntegerField(default=0, editable=False)
    update_date = models.DateTimeField("Дата создания", auto_now=True)
    create_date = models.DateTimeField("Дата редактирования", auto_now_add=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        self.reading_time = calculate_reading_time(self.text)
        super().save(*args, **kwargs)

    class Meta:
        managed = False
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        db_table = "post"


class Quiz(models.Model):
    title = models.CharField("Название", max_length=100)
    description = models.TextField("Описание", blank=True, null=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        managed = False
        db_table = "quiz"
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"


class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, models.CASCADE, verbose_name="Тест")
    title = MDTextField("Текст вопроса")
    hint = models.CharField("Подсказка", max_length=200, blank=True, null=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        managed = False
        db_table = "quiz_question"
        verbose_name = "Вопрос к тесту"
        verbose_name_plural = "Вопросы к тесту"


class QuizAnswer(models.Model):
    question = models.ForeignKey(QuizQuestion, models.CASCADE)
    title = models.CharField("Ответ", max_length=100)
    is_correct = models.BooleanField("Правильный?", default=False)
    explanation = models.TextField("Объсянение", max_length=200, blank=True, null=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        managed = False
        db_table = "quiz_answer"
        verbose_name = "Ответ к тесту"
        verbose_name_plural = "Ответы к тесту"
