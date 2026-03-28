from __future__ import annotations

from typing import Any

from django.conf import settings

DEFAULTS = {
    "RENDERER_CLASS": "django_markdown_widget.renderers.DefaultRenderer",
    "UPLOAD_HANDLER_CLASS": "django_markdown_widget.uploads.DefaultUploadHandler",
    "TOOLBAR": [
        # Text formatting
        "bold", "italic", "strikethrough", "highlight",
        "separator",
        # Headings & structure
        "heading", "quote", "horizontal-rule",
        "separator",
        # Code
        "code", "code-block",
        "separator",
        # Lists
        "unordered-list", "ordered-list", "task-list",
        "separator",
        # Links & media
        "link", "image", "video", "document",
        "separator",
        # Rich blocks
        "table", "details", "embed",
        "separator",
        # Extras
        "superscript", "subscript",
        "separator",
        # Actions (right-aligned)
        "undo", "redo",
    ],
    "ALLOWED_UPLOAD_TYPES": [
        # Images
        "image/png",
        "image/jpeg",
        "image/gif",
        "image/webp",
        # Videos
        "video/mp4",
        "video/webm",
        "video/ogg",
        # Documents
        "application/pdf",
        "application/zip",
        "application/x-tar",
        "application/gzip",
        "text/plain",
        "text/csv",
        "application/json",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ],
    "MAX_UPLOAD_SIZE": 50 * 1024 * 1024,
    "UPLOAD_PATH": "md-editor/uploads/%Y/%m/",
    "TEMP_UPLOAD_PATH": "md-editor/tmp/",
    "TEMP_MAX_AGE": 24 * 60 * 60,
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
