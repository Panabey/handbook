from django.http import FileResponse, HttpRequest
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET


@require_GET
@cache_control(public=True, max_age=315360000)
def favicon(request: HttpRequest):
    return FileResponse(open("favicon.ico", "rb"))
