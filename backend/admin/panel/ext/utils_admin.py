import os
import re
import math

from threading import Lock
from django.conf import settings


def calculate_reading_time(text: str, char_per_second: int = 1200) -> int:
    characters = len(text)
    minutes = math.ceil(characters / char_per_second)
    return minutes


def replace_char(pattern: str, text: str) -> str:
    return re.sub(pattern, " ", text)


def find_image(markdown_text: str):
    return re.findall(r"!\[.*?\]\((/media/.*?)\)", markdown_text)


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
            if os.path.exists(image_path):
                os.remove(image_path)
        finally:
            lock.release()


def get_text_or_none(classmodel, pk):
    try:
        return classmodel.objects.using("handbook").get(pk=pk).text
    except classmodel.DoesNotExist:
        return None
