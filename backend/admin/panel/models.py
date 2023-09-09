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
import threading

from typing import Collection
from django.db import models
from django.core.exceptions import ValidationError

from mdeditor.fields import MDTextField
from colorfield.fields import ColorField

from .ext.utils_admin import replace_char
from .ext.utils_admin import remove_old_images
from .ext.utils_admin import calculate_reading_time

from core.storage import CompressImageStorage
from django_cleanup import cleanup


class TagStatus(models.Model):
    title = models.CharField("Название статуса", max_length=60)

    def __str__(self) -> str:
        return self.title

    def clean_fields(self, exclude: Collection[str] | None) -> None:
        existing_value = (
            Tag.objects.using("handbook")
            .filter(title=self.title)
            .exclude(pk=self.pk)
            .first()
        )
        if existing_value:
            raise ValidationError({"title": "Статус уже существует"})
        return super().clean_fields(exclude)

    class Meta:
        managed = False
        db_table = "tag_status"
        verbose_name = "Статус тег"
        verbose_name_plural = "Статус теги"


class Tag(models.Model):
    title = models.CharField("Название тега", max_length=60)
    status = models.ForeignKey("TagStatus", models.CASCADE, verbose_name="Статус")

    def __str__(self) -> str:
        return f"{self.title} ({self.status})"

    def clean_fields(self, exclude: Collection[str] | None) -> None:
        existing_value = (
            Tag.objects.using("handbook")
            .filter(title=self.title)
            .exclude(pk=self.pk)
            .first()
        )
        if existing_value:
            raise ValidationError({"title": "Тег уже существует"})
        return super().clean_fields(exclude)

    class Meta:
        managed = False
        db_table = "tag"
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ["-id"]


class HandBookStatus(models.Model):
    title = models.CharField(max_length=25, verbose_name="Название статуса")
    color_text = ColorField("Цвет текста", default="#5573f3")
    color_background = ColorField("Цвет фона", default="#e2e8ff")

    def __str__(self) -> str:
        return self.title

    def clean_fields(self, exclude: Collection[str] | None) -> None:
        existing_value = (
            HandBookStatus.objects.using("handbook")
            .filter(title=self.title)
            .exclude(pk=self.pk)
            .first()
        )
        if existing_value:
            raise ValidationError({"title": "Топик уже существует"})
        return super().clean_fields(exclude)

    class Meta:
        managed = False
        verbose_name = "Справочник (Статус)"
        verbose_name_plural = "Справочник (Статусы)"
        db_table = "handbook_status"


@cleanup.select
class Handbook(models.Model):
    logo_url = models.FileField(
        "Изображение",
        upload_to="handbook/",
        blank=True,
        null=True,
        storage=CompressImageStorage,
    )
    title = models.CharField("Название справочника", max_length=80)
    description = models.TextField("Описание", max_length=255, blank=True, null=True)
    status = models.ForeignKey(
        "HandBookStatus", models.SET_NULL, blank=True, null=True, verbose_name="Статус"
    )

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        self.title = replace_char(r"[-\s]+", self.title.strip())
        super().save(*args, **kwargs)

    def clean_fields(self, exclude: Collection[str] | None) -> None:
        existing_value = (
            Handbook.objects.using("handbook")
            .filter(title=self.title)
            .exclude(pk=self.pk)
            .first()
        )
        if existing_value:
            raise ValidationError({"title": "Справочник уже существует"})
        return super().clean_fields(exclude)

    class Meta:
        managed = False
        verbose_name = "Справочник"
        verbose_name_plural = "Справочники"
        db_table = "handbook"
        ordering = ["-id"]


class HandbookContent(models.Model):
    handbook = models.ForeignKey(Handbook, models.CASCADE, verbose_name="Справочник")
    title = models.CharField(
        "Раздел справочника", help_text="Например: 1. Основы", max_length=80
    )
    description = models.TextField("Описание раздела", max_length=255)

    def __str__(self) -> str:
        return f"{self.title} ({self.handbook.title})"

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
        verbose_name = "Справочники (Раздел)"
        verbose_name_plural = "Справочники (Разделы)"
        db_table = "handbook_content"
        ordering = ["-id"]


class HandbookPage(models.Model):
    content = models.ForeignKey(HandbookContent, models.CASCADE, verbose_name="Раздел")
    title = models.CharField(
        "Название темы", help_text="Например: 1.1 Циклы", max_length=80
    )
    short_description = models.TextField(
        "Короткое описание",
        help_text="Так же используется для мета тегов",
        max_length=160,
    )
    text = MDTextField("Текст")
    reading_time = models.IntegerField(default=0, editable=False)
    update_date = models.DateTimeField("Дата редактирования", auto_now=True)
    create_date = models.DateTimeField("Дата создания", auto_now_add=True)

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
        old_text = HandbookPage.objects.using("handbook").get(pk=self.pk).text

        super().save(*args, **kwargs)
        thread = threading.Thread(target=remove_old_images, args=(old_text, self.text))
        thread.start()

    class Meta:
        managed = False
        verbose_name = "Справочник (Страница)"
        verbose_name_plural = "Справочник (Страницы)"
        db_table = "handbook_page"


@cleanup.select
class Article(models.Model):
    logo_url = models.FileField(
        "Изображение",
        upload_to="articles/",
        blank=True,
        null=True,
        storage=CompressImageStorage,
    )
    title = models.CharField("Название поста", max_length=80)
    anons = models.TextField("Краткое содержание", max_length=255)
    text = MDTextField("Текст")
    reading_time = models.IntegerField(default=0, editable=False)
    update_date = models.DateTimeField("Дата редактирования", auto_now=True)
    create_date = models.DateTimeField("Дата создания", auto_now_add=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        self.reading_time = calculate_reading_time(self.text)
        old_text = Article.objects.using("handbook").get(pk=self.pk).text

        super().save(*args, **kwargs)
        thread = threading.Thread(target=remove_old_images, args=(old_text, self.text))
        thread.start()

    class Meta:
        managed = False
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        db_table = "article"


class ArticleTag(models.Model):
    article = models.ForeignKey(Article, models.CASCADE)
    tag = models.ForeignKey(Tag, models.CASCADE)

    def __str__(self) -> str:
        return "Тег квизов"

    class Meta:
        managed = False
        db_table = "article_tag"


class QuizTopic(models.Model):
    title = models.CharField("Название", max_length=60)

    def __str__(self) -> str:
        return self.title

    def clean_fields(self, exclude: Collection[str] | None) -> None:
        existing_value = (
            QuizTopic.objects.using("handbook")
            .filter(title=self.title)
            .exclude(pk=self.pk)
            .first()
        )
        if existing_value:
            raise ValidationError({"title": "Топик уже существует"})
        return super().clean_fields(exclude)

    class Meta:
        managed = False
        db_table = "quiz_topic"
        verbose_name = "Квиз (Топик)"
        verbose_name_plural = "Квиз (Топики)"
        ordering = ["-id"]


@cleanup.select
class Quiz(models.Model):
    topic = models.ForeignKey(
        QuizTopic, models.CASCADE, verbose_name="Тема", null=True, blank=True
    )
    logo_url = models.FileField(
        "Изображение",
        upload_to="quiz",
        blank=True,
        null=True,
        storage=CompressImageStorage,
    )
    title = models.CharField("Название", max_length=100)
    short_description = models.TextField(
        "Короткое опписание",
        help_text="Так же используется для мета тегов",
        max_length=160,
    )
    description = MDTextField("Описание", blank=True, null=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        managed = False
        db_table = "quiz"
        verbose_name = "Квиз"
        verbose_name_plural = "Квизы"
        ordering = ["-id"]


class QuizTag(models.Model):
    quiz = models.ForeignKey(Quiz, models.CASCADE)
    tag = models.ForeignKey(Tag, models.CASCADE)

    def __str__(self) -> str:
        return "Тег квизов"

    class Meta:
        managed = False
        db_table = "quiz_tag"


class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, models.CASCADE, verbose_name="Тест")
    text = MDTextField("Текст вопроса", max_length=255)
    hint = models.CharField("Подсказка", max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return self.text

    class Meta:
        managed = False
        db_table = "quiz_question"
        verbose_name = "Квиз (Вопрос)"
        verbose_name_plural = "Квиз (Вопросы)"


class QuizAnswer(models.Model):
    question = models.ForeignKey(QuizQuestion, models.CASCADE)
    text = models.CharField("Ответ", max_length=255)
    is_correct = models.BooleanField("Правильный?", default=False)
    explanation = models.TextField("Объсянение", max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return self.text

    class Meta:
        managed = False
        db_table = "quiz_answer"
        verbose_name = "Квиз (Ответ)"
        verbose_name_plural = "Квиз (Ответы)"
