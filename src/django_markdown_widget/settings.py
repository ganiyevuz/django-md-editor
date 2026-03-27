from __future__ import annotations

from typing import Any

from django.conf import settings

DEFAULTS = {
    "RENDERER_CLASS": "django_markdown_widget.renderers.DefaultRenderer",
    "UPLOAD_HANDLER_CLASS": "django_markdown_widget.uploads.DefaultUploadHandler",
    "TOOLBAR": [
        "heading",
        "bold",
        "italic",
        "strikethrough",
        "separator",
        "quote",
        "code",
        "code-block",
        "link",
        "image",
        "separator",
        "ordered-list",
        "unordered-list",
        "task-list",
        "separator",
        "horizontal-rule",
        "table",
        "details",
        "separator",
        "highlight",
        "superscript",
        "subscript",
        "separator",
        "attach",
        "mention",
        "ref",
        "separator",
        "undo",
        "redo",
        "fullscreen",
    ],
    "ALLOWED_UPLOAD_TYPES": [
        "image/png",
        "image/jpeg",
        "image/gif",
        "image/webp",
    ],
    "MAX_UPLOAD_SIZE": 10 * 1024 * 1024,
    "UPLOAD_PATH": "md-editor/uploads/%Y/%m/",
    "CLIENT_RENDERER": "django_markdown_widget/js/marked.min.js",
    "DEFAULT_HEIGHT": "300px",
    "PLACEHOLDER": "Add your comment here...",
    "REQUIRE_AUTH": True,
    "THEME": "auto",
    "CLEANUP_MEDIA": False,
}


def get_setting(key: str) -> Any:
    if key not in DEFAULTS:
        raise KeyError(f"Unknown django-markdown-widget setting: {key}")
    user_settings = getattr(settings, "MD_EDITOR", {})
    return user_settings.get(key, DEFAULTS[key])
