# API Reference

## Public Classes

### `MarkdownEditorWidget`

:   Django form widget. Extends `django.forms.widgets.Textarea`.

    ```python
    from django_md_editor import MarkdownEditorWidget
    ```

    **Parameters:** `toolbar`, `preview_url`, `upload_url`, `height`, `placeholder`, `attrs`

### `MarkdownEditorAdminMixin`

:   ModelAdmin mixin. Add before `admin.ModelAdmin` in the MRO.

    ```python
    from django_md_editor import MarkdownEditorAdminMixin
    ```

    **Attributes:**

    - `markdown_fields` -- `list[str] | None`. `None` applies to all TextFields.

### `MarkdownCleanupMixin`

:   Abstract model mixin. Deletes orphaned media on `save()`.

    ```python
    from django_md_editor import MarkdownCleanupMixin
    ```

    **Attributes:**

    - `markdown_cleanup_fields` -- `list[str] | None`. `None` tracks all TextFields.

### `BaseRenderer`

:   Abstract base class for server-side markdown renderers.

    ```python
    from django_md_editor import BaseRenderer
    ```

    **Abstract methods:**

    - `render(markdown_text: str) -> str`

### `DefaultRenderer`

:   Default renderer using python-markdown. Falls back to HTML-escaped text.

    ```python
    from django_md_editor import DefaultRenderer
    ```

### `BaseUploadHandler`

:   Abstract base class for file upload handlers.

    ```python
    from django_md_editor import BaseUploadHandler
    ```

    **Methods:**

    - `validate(file: UploadedFile) -> None` -- override to add validation. Raise `ValidationError` to reject.
    - `save(file: UploadedFile) -> str` -- *abstract*. Store the file and return its URL.

### `DefaultUploadHandler`

:   Default handler using Django's `default_storage`.

    ```python
    from django_md_editor import DefaultUploadHandler
    ```

## Utility Functions

### `extract_media_urls(text: str) -> set[str]`

:   Extract all `![alt](url)` image URLs from markdown text.

    ```python
    from django_md_editor import extract_media_urls

    urls = extract_media_urls("Hello ![img](/media/uploads/photo.png)")
    # {"/media/uploads/photo.png"}
    ```

### `delete_orphaned_media(old_text: str, new_text: str) -> list[str]`

:   Compare old and new markdown, delete files removed from content. Returns list of deleted storage paths.

    ```python
    from django_md_editor import delete_orphaned_media

    deleted = delete_orphaned_media(old_content, new_content)
    ```

### `get_setting(key: str) -> Any`

:   Retrieve a setting value with fallback to defaults.

    ```python
    from django_md_editor.settings import get_setting

    max_size = get_setting("MAX_UPLOAD_SIZE")
    ```

    Raises `KeyError` for unrecognized setting names.

## URL Endpoints

Both endpoints are registered under the `django_md_editor` app namespace.

### `POST /md-editor/preview`

:   Render markdown to HTML.

    **Request body** (JSON): `{"text": "**bold**"}`

    **Response**: `{"html": "<p><strong>bold</strong></p>"}`

    Requires authentication by default (`REQUIRE_AUTH`).

### `POST /md-editor/upload`

:   Upload a file.

    **Request**: multipart form with `file` field.

    **Response**: `{"url": "/media/md-editor/uploads/2026/03/1234_photo.png", "name": "photo.png"}`

    Requires authentication by default (`REQUIRE_AUTH`).

## Template Tags & Filters

Load with `{% load md_editor %}`.

### `{% markdown text %}`

:   Render markdown text as HTML (simple tag).

### `{{ text|markdown }}`

:   Render markdown text as HTML (filter).
