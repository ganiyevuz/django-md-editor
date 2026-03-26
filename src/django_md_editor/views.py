import json

from django.http import JsonResponse
from django.utils.module_loading import import_string
from django.views import View

from django_md_editor.settings import get_setting


def load_renderer():
    renderer_class = import_string(get_setting("RENDERER_CLASS"))
    return renderer_class()


def load_upload_handler():
    handler_class = import_string(get_setting("UPLOAD_HANDLER_CLASS"))
    return handler_class()


class PreviewView(View):
    http_method_names = ["post"]

    def dispatch(self, request, *args, **kwargs):
        if get_setting("REQUIRE_AUTH") and not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=403)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        try:
            body = json.loads(request.body)
            text = body.get("text", "")
        except (json.JSONDecodeError, AttributeError):
            text = request.POST.get("text", "")

        renderer = load_renderer()
        html = renderer.render(text)
        return JsonResponse({"html": html})


class UploadView(View):
    http_method_names = ["post"]

    def dispatch(self, request, *args, **kwargs):
        if get_setting("REQUIRE_AUTH") and not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=403)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return JsonResponse({"error": "No file provided"}, status=400)

        handler = load_upload_handler()
        try:
            handler.validate(file)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

        url = handler.save(file)
        return JsonResponse({"url": url, "name": file.name})
