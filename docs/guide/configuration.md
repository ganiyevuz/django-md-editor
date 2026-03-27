# Configuration

All settings are optional. Configure them under the `MD_EDITOR` dictionary in your Django settings.

```python
MD_EDITOR = {
    "RENDERER_CLASS": "django_markdown_widget.renderers.DefaultRenderer",
    "UPLOAD_HANDLER_CLASS": "django_markdown_widget.uploads.DefaultUploadHandler",
    "TOOLBAR": ["heading", "bold", "italic", ...],
    "ALLOWED_UPLOAD_TYPES": ["image/png", "image/jpeg", "image/gif", "image/webp"],
    "MAX_UPLOAD_SIZE": 10 * 1024 * 1024,
    "UPLOAD_PATH": "md-editor/uploads/%Y/%m/",
    "CLIENT_RENDERER": "django_markdown_widget/js/marked.min.js",
    "DEFAULT_HEIGHT": "300px",
    "PLACEHOLDER": "Add your comment here...",
    "THEME": "auto",
    "REQUIRE_AUTH": True,
    "CLEANUP_MEDIA": False,
}
```

## Settings Reference

### `RENDERER_CLASS`

: **Default:** `"django_markdown_widget.renderers.DefaultRenderer"`

  Dotted Python path to the server-side markdown renderer class. Must extend `BaseRenderer`.

### `UPLOAD_HANDLER_CLASS`

: **Default:** `"django_markdown_widget.uploads.DefaultUploadHandler"`

  Dotted Python path to the upload handler class. Must extend `BaseUploadHandler`.

### `TOOLBAR`

: **Default:** Full toolbar with all available buttons

  List of toolbar button names. Use `"separator"` to add visual dividers. See [Toolbar Customization](../customization/toolbar.md) for available buttons.

### `ALLOWED_UPLOAD_TYPES`

: **Default:** `["image/png", "image/jpeg", "image/gif", "image/webp"]`

  MIME types accepted for file uploads.

### `MAX_UPLOAD_SIZE`

: **Default:** `10485760` (10 MB)

  Maximum upload file size in bytes.

### `UPLOAD_PATH`

: **Default:** `"md-editor/uploads/%Y/%m/"`

  Storage path for uploaded files. Supports `strftime` format codes for date-based directories.

### `CLIENT_RENDERER`

: **Default:** `"django_markdown_widget/js/marked.min.js"`

  Path to the client-side markdown renderer JavaScript file (served as a static file).

### `DEFAULT_HEIGHT`

: **Default:** `"300px"`

  Default CSS height for the editor. Can be overridden per widget instance.

### `PLACEHOLDER`

: **Default:** `"Add your comment here..."`

  Default placeholder text. Can be overridden per widget instance.

### `THEME`

: **Default:** `"auto"`

  Editor theme. Options: `"light"`, `"dark"`, `"auto"` (follows system preference).

### `REQUIRE_AUTH`

: **Default:** `True`

  When `True`, the preview and upload endpoints require authenticated users. Set to `False` for public-facing forms.

### `CLEANUP_MEDIA`

: **Default:** `False`

  When `True`, the `MarkdownCleanupMixin` actively deletes orphaned media files on model save. See [Media Cleanup](cleanup.md).
