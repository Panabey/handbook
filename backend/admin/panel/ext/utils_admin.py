import os
import re
import math

from typing import Any, NoReturn
from threading import Lock

from django.db import models
from django.conf import settings as django_settings
from django.core.exceptions import ValidationError

from core.settings import settings


def calculate_reading_time(text: str, char_per_second: int = 1200) -> int:
    """Функция подсчёта времени для чтения текста"""
    characters = len(text)
    minutes = math.ceil(characters / char_per_second)
    return minutes


def replace_char(pattern: str, text: str) -> str:
    """Функция замены символов по шаблону"""
    return re.sub(pattern, " ", text)


def find_image(markdown_text: str):
    """Функция поиска изображений в тексте markdown или html"""
    pattern = r"\/general\/[^\/]+\/[^\/]+\.\w+"
    # Поиск пути к изображениям в тексте
    matches = re.findall(pattern, markdown_text)
    return matches


def remove_old_images(old_text: str, new_text: str):
    """Функция удаления изображений, которые не присустсвуют в тексте при сохранении"""
    lock = Lock()
    old_images = find_image(old_text)
    new_images = find_image(new_text)
    print(old_images, new_images)
    # Поиск изображений, которые были удалены при изменении текста
    missing_images = [image for image in old_images if image not in new_images]
    for image in missing_images:
        image_path = django_settings.MEDIA_ROOT / image.lstrip("/")
        lock.acquire()
        try:
            parent_dir = os.path.dirname(image_path)
            if os.path.exists(image_path):
                os.remove(image_path)

            if not os.listdir(parent_dir):
                os.rmdir(parent_dir)
        except OSError:
            pass
        lock.release()


def get_text_or_none(classmodel: models.Model, pk: int, field_name: str) -> Any | None:
    """Функция получния текста, если тот существует"""
    try:
        data = (
            classmodel.objects.using(settings.DB_BACKEND_NAME)
            .values_list(field_name)
            .get(pk=pk)
        )
        return data[0]
    except classmodel.DoesNotExist:
        return None


def validate_uint(value: int) -> None | NoReturn:
    """Функция валидации отрицательных чисел"""
    if value < 1:
        raise ValidationError("Убедитесь, что это значение больше либо равно 1.")


def validate_english_letters(value: str) -> None | NoReturn:
    if not re.match("^[a-zA-Z ]+$", value):
        raise ValidationError(
            "Текст должен содержать только английские буквы и/или пробелы."
        )


def validate_exist(classmodel: models.Model, fields: dict[str, Any]) -> bool:
    """Функция проверки на существующие значения в БД"""
    data = classmodel.objects.using(settings.DB_BACKEND_NAME).filter(**fields).exists()
    if data:
        return True
    return False


def validate_count(
    classmodel: models.Model, fields: dict[str, Any], max_count: int
) -> bool:
    """Функция проверки надопустимое количество элементов в БД"""
    count_data = (
        classmodel.objects.using(settings.DB_BACKEND_NAME).filter(**fields).count()
    )
    if count_data >= max_count:
        return False
    return True
