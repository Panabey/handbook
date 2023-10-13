import threading

from django.db import models

from mdeditor.fields import MDTextField
from colorfield.fields import ColorField

from .ext.utils_admin import replace_char
from .ext.utils_admin import validate_uint
from .ext.utils_admin import get_text_or_none
from .ext.utils_admin import remove_old_images
from .ext.utils_admin import calculate_reading_time

from core.storage import CompressImageStorage
from django_cleanup import cleanup


class TagStatus(models.Model):
    title = models.CharField("Название статуса", max_length=60, unique=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        managed = False
        db_table = "tag_status"
        verbose_name = "Статус тег"
        verbose_name_plural = "Статус теги"


class Tag(models.Model):
    title = models.CharField("Название тега", max_length=60, unique=True)
    status = models.ForeignKey("TagStatus", models.CASCADE, verbose_name="Статус")

    def __str__(self) -> str:
        return f"{self.title} ({self.status})"

    class Meta:
        managed = False
        db_table = "tag"
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class HandBookStatus(models.Model):
    title = models.CharField(
        max_length=40, verbose_name="Название статуса", unique=True
    )
    color_text = ColorField("Цвет текста", default="#5573f3")
    color_background = ColorField("Цвет фона", default="#e2e8ff")

    def __str__(self) -> str:
        return self.title

    class Meta:
        managed = False
        verbose_name = "Справочник (Статус)"
        verbose_name_plural = "Справочник (Статусы)"
        db_table = "handbook_status"


class HandbookCategory(models.Model):
    title = models.CharField(
        "Название категории справочников", max_length=80, unique=True
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        managed = False
        verbose_name = "Справочник (Категории)"
        verbose_name_plural = "Справочник (Категория)"
        db_table = "handbook_category"


@cleanup.select
class Handbook(models.Model):
    logo_url = models.FileField(
        "Изображение",
        upload_to="handbook/",
        blank=True,
        null=True,
        storage=CompressImageStorage,
    )
    title = models.CharField("Название справочника", max_length=80, unique=True)
    description = models.TextField("Описание", max_length=300, blank=True, null=True)
    is_visible = models.BooleanField("Видимый?", default=False)
    category = models.ForeignKey(
        "HandbookCategory",
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Категория",
    )
    status = models.ForeignKey(
        "HandBookStatus", models.SET_NULL, blank=True, null=True, verbose_name="Статус"
    )

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        self.title = replace_char(r"[-\s]+", self.title.strip())
        super().save(*args, **kwargs)

    class Meta:
        managed = False
        verbose_name = "Справочник"
        verbose_name_plural = "Справочники"
        db_table = "handbook"


class HandbookContent(models.Model):
    handbook = models.ForeignKey(Handbook, models.CASCADE, verbose_name="Справочник")
    part = models.SmallIntegerField(
        "Номер раздела справочника",
        help_text="Например: 1",
        validators=[
            validate_uint,
        ],
    )
    title = models.CharField(
        "Название раздела справочника", help_text="Например: Основы", max_length=80
    )
    description = models.TextField("Описание раздела", max_length=400)

    def __str__(self) -> str:
        return f"{self.part}. {self.title} ({self.handbook.title})"

    class Meta:
        managed = False
        verbose_name = "Справочники (Раздел)"
        verbose_name_plural = "Справочники (Разделы)"
        db_table = "handbook_content"


class HandbookPage(models.Model):
    content = models.ForeignKey(HandbookContent, models.CASCADE, verbose_name="Раздел")
    subpart = models.SmallIntegerField(
        "Номер темы раздела справочника",
        help_text="Например: 1",
        validators=[
            validate_uint,
        ],
    )
    title = models.CharField(
        "Название темы", help_text="Например: Циклы", max_length=80
    )
    short_description = models.TextField(
        "Короткое описание",
        help_text="Так же используется для мета тегов",
        max_length=255,
    )
    text = MDTextField("Текст")
    reading_time = models.IntegerField(default=0, editable=False)
    update_date = models.DateTimeField("Дата редактирования", auto_now=True)
    create_date = models.DateTimeField("Дата создания", auto_now_add=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        self.reading_time = calculate_reading_time(self.text)
        old_text = get_text_or_none(HandbookPage, self.pk, "text")

        super().save(*args, **kwargs)
        if old_text:
            thread = threading.Thread(
                target=remove_old_images, args=(old_text, self.text)
            )
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
    title = models.CharField("Название поста", max_length=120)
    anons = models.TextField("Краткое содержание", max_length=400)
    text = MDTextField("Текст")
    reading_time = models.IntegerField(default=0, editable=False)
    update_date = models.DateTimeField("Дата редактирования", auto_now=True)
    create_date = models.DateTimeField("Дата создания", auto_now_add=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        self.reading_time = calculate_reading_time(self.text)
        old_text = get_text_or_none(Article, self.pk, "text")

        super().save(*args, **kwargs)
        if old_text:
            thread = threading.Thread(
                target=remove_old_images, args=(old_text, self.text)
            )
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
        return "Тег статьи"

    class Meta:
        managed = False
        db_table = "article_tag"


class QuizTopic(models.Model):
    title = models.CharField("Название", max_length=80, unique=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        managed = False
        db_table = "quiz_topic"
        verbose_name = "Квиз (Топик)"
        verbose_name_plural = "Квиз (Топики)"


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
        max_length=255,
    )
    description = MDTextField("Описание", max_length=500, blank=True, null=True)
    is_visible = models.BooleanField(
        "Видимый?", default=False, help_text="Не скрывает вопросы и ответы"
    )

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        old_description = get_text_or_none(Quiz, self.pk, "description")

        super().save(*args, **kwargs)
        if old_description:
            thread = threading.Thread(
                target=remove_old_images, args=(old_description, self.description)
            )
            thread.start()

    class Meta:
        managed = False
        db_table = "quiz"
        verbose_name = "Квиз"
        verbose_name_plural = "Квизы"


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
    text = MDTextField("Текст вопроса", max_length=400)
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
    explanation = models.TextField("Объсянение", max_length=300, blank=True, null=True)

    def __str__(self) -> str:
        return self.text

    class Meta:
        managed = False
        db_table = "quiz_answer"
        verbose_name = "Квиз (Ответ)"
        verbose_name_plural = "Квиз (Ответы)"


class ProjectNews(models.Model):
    title = models.CharField("Заголовок", max_length=80)
    text = MDTextField("Текст")
    reading_time = models.IntegerField(default=0, editable=False)
    create_date = models.DateTimeField("Дата создания", auto_now_add=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        self.reading_time = calculate_reading_time(self.text)
        old_text = get_text_or_none(ProjectNews, self.pk, "text")

        super().save(*args, **kwargs)
        if old_text:
            thread = threading.Thread(
                target=remove_old_images, args=(old_text, self.text)
            )
            thread.start()

    class Meta:
        managed = False
        db_table = "project_news"
        verbose_name = "Новость проекта"
        verbose_name_plural = "Новости проекта"
