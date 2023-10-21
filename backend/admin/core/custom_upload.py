import os
import string
import random
import datetime

from PIL import Image
from pathlib import Path
from slugify import slugify

from django.conf import settings
from django.views import generic
from django.http import HttpRequest
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.files.uploadedfile import UploadedFile
from django.views.decorators.clickjacking import xframe_options_sameorigin

from mdeditor.configs import MDConfig

MDEDITOR_CONFIGS = MDConfig("default")


class UploadView(generic.View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    @xframe_options_sameorigin
    def post(self, request: HttpRequest, *args, **kwargs):
        upload_image = request.FILES.get("editormd-image-file", None)
        media_root = settings.MEDIA_ROOT

        # Если изображение не существует или не было получено
        if not upload_image:
            return JsonResponse({
                "success": 0, "message": "未获取到要上传的图片", "url": ""
            })  # fmt: skip

        # Проверка допустимого формата изображения
        file_path = self.normalize_filename(Path(upload_image.name))
        ext = file_path.suffix

        if ext not in MDEDITOR_CONFIGS["upload_image_formats"]:
            return JsonResponse(
                {
                    "success": 0,
                    "message": "上传图片格式错误，允许上传图片格式为：%s"
                    % ",".join(MDEDITOR_CONFIGS["upload_image_formats"]),
                    "url": "",
                }
            )

        # Получение папки в соотвествии с текущей датой
        date = datetime.datetime.utcnow().strftime("%Y-%m-%d")
        save_dir = os.path.join(media_root, MDEDITOR_CONFIGS["image_folder"], date)
        os.makedirs(save_dir, exist_ok=True)

        # Сохранение изображения
        if ext not in [".svg", ".gif", ".bmp", ".webp"]:
            relative_filename = self._compress_img(
                upload_image, file_path, save_dir, 0.9
            )
        else:
            relative_filename = self._no_compress_img(upload_image, file_path, save_dir)

        path_url = os.path.join(
            settings.MEDIA_URL,
            MDEDITOR_CONFIGS["image_folder"],
            date,
            relative_filename,
        ).replace("\\", "/")
        return JsonResponse({"success": 1, "message": "上传成功！", "url": path_url})

    def _compress_img(
        self,
        image: UploadedFile,
        file_path: Path,
        save_dir: str,
        new_size_ratio: float = 0.9,
        quality: int = 90,
        width: int | None = None,
        height: int | None = None,
    ) -> str:
        """Оптимизация полученного изображения для уменьшения его размера
        с последующим сохранением
        """
        img = Image.open(image)

        if new_size_ratio < 1.0:
            # Если коэффициент изменения размера ниже 1.0, умножить ширину и
            # высоту на этот коэффициент, чтобы уменьшить размер изображения.
            img = img.resize(
                (int(img.size[0] * new_size_ratio), int(img.size[1] * new_size_ratio)),
                Image.BILINEAR,
            )
        elif width and height:
            img = img.resize((width, height), Image.BILINEAR)

        relative_filename = self.generate_filename(save_dir, file_path, True)

        # Конвертация прозрачности в белый цвет
        if img.mode == "LA":
            img = img.convert("RGBA")
        if img.mode == "RGBA":
            new_image = Image.new("RGB", img.size, (255, 255, 255))
            new_image.paste(img, mask=img.split()[3])
            img = new_image

        img.save(
            os.path.join(save_dir, relative_filename),
            format="JPEG",
            quality=quality,
            optimize=True,
            exif=b"",
            progressive=True,
        )
        img.close()

        return relative_filename

    def _no_compress_img(self, image: UploadedFile, filename: Path, save_path: str):
        """Сохранение изображения без последующей оптимизации"""
        file_fullname = self.generate_filename(save_path, filename, False)

        with open(os.path.join(save_path, file_fullname), "wb") as file:
            for chunk in image.chunks():
                file.write(chunk)

        return file_fullname

    def generate_filename(
        self, save_dir: str, file_path: Path, is_compress: bool
    ) -> str:
        """Генерация имени изображения для последующего сохранения"""
        if is_compress:
            file_path = file_path.with_suffix(".jpeg")
        full_path = os.path.join(save_dir, file_path.name)

        # Если файл с таким именем уже существует добавить случайные данные в путь
        if os.path.exists(full_path):
            random_choice = "".join(
                random.choices(string.ascii_lowercase + string.digits, k=6)
            )
            relative_filename = f"{file_path.stem}-{random_choice}{file_path.suffix}"
        else:
            relative_filename = file_path.name
        return relative_filename

    def normalize_filename(self, file_path: Path) -> Path:
        """Удаление символов, которые могут повлять на отображение/сохранение"""
        # Исключает специальные символы и заменяет пробелы на подчёркивания
        filename = slugify(file_path.stem, max_length=255)
        filename = filename + file_path.suffix
        return file_path.parent / filename
