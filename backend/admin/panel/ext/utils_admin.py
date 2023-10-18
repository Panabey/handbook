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
    combined_pattern = r'!\[.*\]\((\/media\/.*?)\)|<img.*?src=["\'](/media\/.*?)["\']'
    # Поиск пути к изображениям в тексте
    matches = re.findall(combined_pattern, markdown_text)
    # Удаление пустых строк полученных при сравнении
    return [match[0] if match[0] else match[1] for match in matches]


def remove_old_images(old_text: str, new_text: str):
    """Функция удаления изображений, которые не присустсвуют в тексте при сохранении"""
    lock = Lock()
    old_images = find_image(old_text)
    new_images = find_image(new_text)

    # Поиск изображений, которые были удалены при изменении текста
    missing_images = [image for image in old_images if image not in new_images]
    for image in missing_images:
        image_path = os.path.join(django_settings.BASE_DIR, image[1:])
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


def validate_exist(classmodel: models.Model, fields: dict[str, Any]) -> bool:
    """Функция проверки на существующие значения в БД"""
    data = classmodel.objects.using(settings.DB_BACKEND_NAME).filter(**fields).exists()
    if data:
        return True
    return False
