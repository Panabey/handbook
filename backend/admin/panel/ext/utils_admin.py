import os
import re
import math

from threading import Lock
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError


def calculate_reading_time(text: str, char_per_second: int = 1200) -> int:
    characters = len(text)
    minutes = math.ceil(characters / char_per_second)
    return minutes


def replace_char(pattern: str, text: str) -> str:
    return re.sub(pattern, " ", text)


def find_image(markdown_text: str):
    combined_pattern = r'!\[.*\]\((\/media\/.*?)\)|<img.*?src=["\'](/media\/.*?)["\']'
    # поиск пути к изображениям
    matches = re.findall(combined_pattern, markdown_text)
    # удаление пустых строк
    return [match[0] if match[0] else match[1] for match in matches]


def remove_old_images(old_text: str, new_text: str):
    lock = Lock()
    old_images = find_image(old_text)
    new_images = find_image(new_text)

    # Находим изображения, которые были удалены из нового текста
    missing_images = [image for image in old_images if image not in new_images]
    for image in missing_images:
        image_path = os.path.join(settings.BASE_DIR, image[1:])
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


def get_text_or_none(classmodel: models.Model, pk: int, field_name: str):
    try:
        data = classmodel.objects.using("handbook").values_list(field_name).get(pk=pk)
        return data[0]
    except classmodel.DoesNotExist:
        return None


def validate_uint(value: int):
    if value < 1:
        raise ValidationError("Убедитесь, что это значение больше либо равно 1.")
