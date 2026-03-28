# Configuration

All settings are optional. Configure them under the `MD_EDITOR` dictionary in your Django settings.

```python
MD_EDITOR = {
    "RENDERER_CLASS": "django_markdown_widget.renderers.DefaultRenderer",
    "UPLOAD_HANDLER_CLASS": "django_markdown_widget.uploads.DefaultUploadHandler",
    "TOOLBAR": ["bold", "italic", "strikethrough", "highlight", ...],
    "ALLOWED_UPLOAD_TYPES": ["image/png", "image/jpeg", "video/mp4", ...],
    "MAX_UPLOAD_SIZE": 50 * 1024 * 1024,
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

## Settings Reference

### `RENDERER_CLASS`

: **Default:** `"django_markdown_widget.renderers.DefaultRenderer"`

  Dotted Python path to the server-side markdown renderer class. Must extend `BaseRenderer`. Output is sanitized to prevent XSS.

### `UPLOAD_HANDLER_CLASS`

: **Default:** `"django_markdown_widget.uploads.DefaultUploadHandler"`

  Dotted Python path to the upload handler class. Must extend `BaseUploadHandler`.

### `TOOLBAR`

: **Default:** Full toolbar grouped by purpose

  List of toolbar button names. Use `"separator"` to add visual dividers. See [Toolbar Customization](../customization/toolbar.md) for available buttons.

### `ALLOWED_UPLOAD_TYPES`

: **Default:** Images (png, jpeg, gif, webp), videos (mp4, webm, ogg), documents (pdf, zip, tar, gz, txt, csv, json, docx, xlsx, pptx)

  MIME types accepted for file uploads. `image/svg+xml` is intentionally excluded from defaults due to XSS risk.

### `MAX_UPLOAD_SIZE`

: **Default:** `52428800` (50 MB)

  Maximum upload file size in bytes.

### `UPLOAD_PATH`

: **Default:** `"md-editor/uploads/%Y/%m/"`

  Permanent storage path for uploaded files. Supports `strftime` format codes.

### `TEMP_UPLOAD_PATH`

: **Default:** `"md-editor/tmp/"`

  Temporary storage path for files during editing. Files are moved to `UPLOAD_PATH` on form submit.

### `TEMP_MAX_AGE`

: **Default:** `86400` (24 hours)

  Maximum age in seconds for temp files. Expired files are deleted by the `cleanup_markdown_media` management command.

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

  When `True`, the upload and finalize endpoints require authenticated users. Set to `False` for public-facing forms.

### `CLEANUP_MEDIA`

: **Default:** `False`

  When `True`, the `MarkdownCleanupMixin` actively deletes orphaned media files on model save. See [Media Cleanup](cleanup.md).
