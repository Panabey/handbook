import os
import datetime

from PIL import Image

from django.conf import settings

from django.views import generic
from django.http import HttpRequest
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.files.uploadedfile import UploadedFile

from mdeditor.configs import MDConfig

MDEDITOR_CONFIGS = MDConfig("default")


class UploadView(generic.View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request: HttpRequest, *args, **kwargs):
        upload_image = request.FILES.get("editormd-image-file", None)
        media_root = settings.MEDIA_ROOT

        # image none check
        if not upload_image:
            return JsonResponse({
                "success": 0, "message": "未获取到要上传的图片", "url": ""
            })  # fmt: skip

        # image format check
        file_name_list = upload_image.name.split(".")
        file_extension = file_name_list.pop(-1)
        file_name = ".".join(file_name_list)

        if file_extension not in MDEDITOR_CONFIGS["upload_image_formats"]:
            return JsonResponse(
                {
                    "success": 0,
                    "message": "上传图片格式错误，允许上传图片格式为：%s"
                    % ",".join(MDEDITOR_CONFIGS["upload_image_formats"]),
                    "url": "",
                }
            )

        # image floder check
        date = datetime.datetime.utcnow().strftime("%Y-%m-%d")
        file_path = os.path.join(media_root, MDEDITOR_CONFIGS["image_folder"], date)
        os.makedirs(file_path, exist_ok=True)

        # save image
        if file_extension != "svg":
            save_filename = self._compress_img(upload_image, file_name, file_path, 0.8)
        else:
            save_filename = self._no_compress_img(upload_image, file_name, file_path)

        path_url = os.path.join(
            settings.MEDIA_URL, MDEDITOR_CONFIGS["image_folder"], date, save_filename
        ).replace("\\", "/")
        return JsonResponse({"success": 1, "message": "上传成功！", "url": path_url})

    def _compress_img(
        self,
        image: UploadedFile,
        filename: str,
        save_path: str,
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
            # если коэффициент изменения размера ниже 1,0, умножить ширину и
            # высоту на этот коэффициент, чтобы уменьшить размер изображения.
            img = img.resize(
                (int(img.size[0] * new_size_ratio), int(img.size[1] * new_size_ratio)),
                Image.BILINEAR,
            )
        elif width and height:
            img = img.resize((width, height), Image.BILINEAR)

        # имя файла
        file_fullname = f"{filename}.jpeg"
        # конвертация прозрачности в белый цвет
        if img.mode == "LA":
            img = img.convert("RGBA")
        if img.mode == "RGBA":
            new_image = Image.new("RGB", img.size, (255, 255, 255))
            new_image.paste(img, mask=img.split()[3])
            img = new_image

        img.save(
            os.path.join(save_path, file_fullname),
            format="JPEG",
            quality=quality,
            optimize=True,
            exif=b"",
        )
        img.close()

        return file_fullname

    def _no_compress_img(self, image: UploadedFile, filename: str, save_path: str):
        """Сохранение изображения без последующей оптимизации"""
        file_fullname = f"{filename}.svg"

        with open(os.path.join(save_path, file_fullname), "wb") as file:
            for chunk in image.chunks():
                file.write(chunk)

        return file_fullname
