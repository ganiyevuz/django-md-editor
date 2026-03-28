# Settings Reference

All settings live under `MD_EDITOR` in your Django settings module.

```python
MD_EDITOR = { ... }
```

Accessing a setting programmatically:

```python
from django_markdown_widget.settings import get_setting

value = get_setting("MAX_UPLOAD_SIZE")  # returns 52428800 if not overridden
```

## Full Defaults

```python
{
    "RENDERER_CLASS": "django_markdown_widget.renderers.DefaultRenderer",
    "UPLOAD_HANDLER_CLASS": "django_markdown_widget.uploads.DefaultUploadHandler",
    "TOOLBAR": [
        "bold", "italic", "strikethrough", "highlight", "separator",
        "heading", "quote", "horizontal-rule", "separator",
        "code", "code-block", "separator",
        "unordered-list", "ordered-list", "task-list", "separator",
        "link", "image", "video", "document", "separator",
        "table", "details", "embed", "separator",
        "superscript", "subscript", "separator",
        "undo", "redo",
    ],
    "ALLOWED_UPLOAD_TYPES": [
        "image/png", "image/jpeg", "image/gif", "image/webp",
        "video/mp4", "video/webm", "video/ogg",
        "application/pdf", "application/zip", "application/x-tar",
        "application/gzip", "text/plain", "text/csv", "application/json",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ],
    "MAX_UPLOAD_SIZE": 52428800,
    "UPLOAD_PATH": "md-editor/uploads/%Y/%m/",
    "TEMP_UPLOAD_PATH": "md-editor/tmp/",
    "TEMP_MAX_AGE": 86400,
    "DEFAULT_HEIGHT": "300px",
    "PLACEHOLDER": "Add your comment here...",
    "THEME": "auto",
    "REQUIRE_AUTH": True,
    "CLEANUP_MEDIA": False,
}
```

Unrecognized keys raise `KeyError` when accessed through `get_setting()`.
