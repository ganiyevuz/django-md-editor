from __future__ import annotations

import json
from functools import cache
from typing import Any

from django.core.exceptions import ValidationError
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.utils.module_loading import import_string
from django.views import View
from django.views.decorators.csrf import csrf_protect

from django_markdown_widget.cleanup import _url_to_temp_path, extract_media_urls
from django_markdown_widget.settings import get_setting


@cache
def _get_upload_handler_class() -> type:
    return import_string(get_setting("UPLOAD_HANDLER_CLASS"))


def load_upload_handler() -> Any:
    """Instantiate the configured upload handler."""
    return _get_upload_handler_class()()


class AuthRequiredMixin:
    """Returns 401 when REQUIRE_AUTH is True and user is unauthenticated."""

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> JsonResponse:
        if get_setting("REQUIRE_AUTH") and not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)
        return super().dispatch(request, *args, **kwargs)


@method_decorator(csrf_protect, name="dispatch")
class UploadView(AuthRequiredMixin, View):
    """Handles file uploads via the configured upload handler."""

    http_method_names = ["post"]

    def post(self, request: HttpRequest) -> JsonResponse:
        file = request.FILES.get("file")
        if not file:
            return JsonResponse({"error": "No file provided"}, status=400)

        handler = load_upload_handler()
        try:
            handler.validate(file)
        except ValidationError as e:
            messages = e.messages if hasattr(e, "messages") else [str(e)]
            return JsonResponse({"error": " ".join(messages)}, status=400)

        url = handler.save(file)
        return JsonResponse({
            "url": url,
            "name": file.name,
            "type": file.content_type or "",
        })


@method_decorator(csrf_protect, name="dispatch")
class FinalizeView(AuthRequiredMixin, View):
    """Moves referenced temp uploads to permanent storage, deletes the rest."""

    http_method_names = ["post"]

    def post(self, request: HttpRequest) -> JsonResponse:
        try:
            body = json.loads(request.body)
            text = body.get("text", "")
        except (json.JSONDecodeError, AttributeError):
            text = request.POST.get("text", "")

        urls = extract_media_urls(text)
        handler = load_upload_handler()
        replacements = {}

        for url in urls:
            temp_path = _url_to_temp_path(url)
            if temp_path:
                new_url = handler.finalize(url)
                if new_url != url:
                    replacements[url] = new_url

        return JsonResponse({"replacements": replacements})
