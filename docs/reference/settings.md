# Settings Reference

All settings live under `MD_EDITOR` in your Django settings module.

```python
MD_EDITOR = { ... }
```

Accessing a setting programmatically:

```python
from django_md_editor.settings import get_setting

value = get_setting("MAX_UPLOAD_SIZE")  # returns 10485760 if not overridden
```

## Full Defaults

```python
{
    "RENDERER_CLASS": "django_md_editor.renderers.DefaultRenderer",
    "UPLOAD_HANDLER_CLASS": "django_md_editor.uploads.DefaultUploadHandler",
    "TOOLBAR": [
        "heading", "bold", "italic", "strikethrough", "separator",
        "quote", "code", "code-block", "link", "image", "separator",
        "ordered-list", "unordered-list", "task-list", "separator",
        "horizontal-rule", "table", "details", "separator",
        "highlight", "superscript", "subscript", "separator",
        "attach", "mention", "ref", "separator",
        "undo", "redo", "fullscreen",
    ],
    "ALLOWED_UPLOAD_TYPES": [
        "image/png",
        "image/jpeg",
        "image/gif",
        "image/webp",
    ],
    "MAX_UPLOAD_SIZE": 10485760,
    "UPLOAD_PATH": "md-editor/uploads/%Y/%m/",
    "CLIENT_RENDERER": "django_md_editor/js/marked.min.js",
    "DEFAULT_HEIGHT": "300px",
    "PLACEHOLDER": "Add your comment here...",
    "THEME": "auto",
    "REQUIRE_AUTH": True,
    "CLEANUP_MEDIA": False,
}
```

Unrecognized keys raise `KeyError` when accessed through `get_setting()`.
