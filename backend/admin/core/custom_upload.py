import os
import datetime

from django.conf import settings
from django.views import generic
from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

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
        file_path = os.path.join(media_root, MDEDITOR_CONFIGS["image_folder"])
        if not os.path.exists(file_path):
            try:
                os.makedirs(file_path)
            except Exception as err:
                return JsonResponse(
                    {"success": 0, "message": "上传失败：%s" % str(err), "url": ""}
                )

        # save image
        utc_date = datetime.datetime.utcnow().strftime("%Y_%m_%d-%H_%M_%S")
        file_full_name = f"{file_name}_{utc_date}.{file_extension}"

        with open(os.path.join(file_path, file_full_name), "wb+") as file:
            for chunk in upload_image.chunks():
                file.write(chunk)

        path_url = os.path.join(
            settings.MEDIA_URL, MDEDITOR_CONFIGS["image_folder"], file_full_name
        )
        return JsonResponse({"success": 1, "message": "上传成功！", "url": path_url})
