# API Reference

## Public Classes

### `MarkdownEditorWidget`

:   Django form widget. Extends `django.forms.widgets.Textarea`.

    ```python
    from django_markdown_widget import MarkdownEditorWidget
    ```

    **Parameters:** `toolbar`, `upload_url`, `finalize_url`, `height`, `placeholder`, `attrs`

### `MarkdownEditorAdminMixin`

:   ModelAdmin mixin. Add before `admin.ModelAdmin` in the MRO.

    ```python
    from django_markdown_widget import MarkdownEditorAdminMixin
    ```

    **Attributes:**

    - `markdown_fields` -- `list[str] | None`. `None` applies to all TextFields.

### `MarkdownCleanupMixin`

:   Abstract model mixin. Deletes orphaned media on `save()`.

    ```python
    from django_markdown_widget import MarkdownCleanupMixin
    ```

    **Attributes:**

    - `markdown_cleanup_fields` -- `list[str] | None`. `None` tracks all TextFields.

### `BaseRenderer`

:   Abstract base class for server-side markdown renderers.

    ```python
    from django_markdown_widget import BaseRenderer
    ```

    **Abstract methods:**

    - `render(markdown_text: str) -> str`

### `DefaultRenderer`

:   Default renderer using python-markdown with HTML sanitization. Falls back to HTML-escaped text if python-markdown is not installed.

    ```python
    from django_markdown_widget import DefaultRenderer
    ```

### `BaseUploadHandler`

:   Abstract base class for file upload handlers.

    ```python
    from django_markdown_widget import BaseUploadHandler
    ```

    **Methods:**

    - `validate(file: UploadedFile) -> None` -- override to add validation. Raise `ValidationError` to reject.
    - `save(file: UploadedFile) -> str` -- *abstract*. Store the file and return its URL.

### `DefaultUploadHandler`

:   Default handler using Django's `default_storage`. Saves to temp storage, with `finalize()` to move to permanent.

    ```python
    from django_markdown_widget import DefaultUploadHandler
    ```

    **Methods:**

    - `save(file) -> str` -- saves to `TEMP_UPLOAD_PATH`, returns URL
    - `finalize(temp_url) -> str` -- moves from temp to `UPLOAD_PATH`, returns new URL

## Utility Functions

### `extract_media_urls(text: str) -> set[str]`

:   Extract all media URLs from markdown text -- images (`![](url)`), links (`[](url)`), and HTML `src` attributes (`<video>`, `<img>`, `<iframe>`).

    ```python
    from django_markdown_widget import extract_media_urls

    urls = extract_media_urls("Hello ![img](/media/uploads/photo.png)")
    # {"/media/uploads/photo.png"}
    ```

### `delete_orphaned_media(old_text: str, new_text: str) -> list[str]`

:   Compare old and new markdown, delete files removed from content. Returns list of deleted storage paths.

    ```python
    from django_markdown_widget import delete_orphaned_media

    deleted = delete_orphaned_media(old_content, new_content)
    ```

### `get_setting(key: str) -> Any`

:   Retrieve a setting value with fallback to defaults.

    ```python
    from django_markdown_widget.settings import get_setting

    max_size = get_setting("MAX_UPLOAD_SIZE")
    ```

    Raises `KeyError` for unrecognized setting names.

## URL Endpoints

Both endpoints are registered under the `django_markdown_widget` app namespace. Protected by `@csrf_protect` and `REQUIRE_AUTH`.

### `POST /md-editor/upload`

:   Upload a file to temp storage.

    **Request**: multipart form with `file` field.

    **Response**: `{"url": "/media/md-editor/tmp/1234_photo.png", "name": "photo.png", "type": "image/png"}`

### `POST /md-editor/finalize`

:   Move referenced temp files to permanent storage.

    **Request body** (JSON): `{"text": "![img](/media/md-editor/tmp/1234_photo.png)"}`

    **Response**: `{"replacements": {"/media/md-editor/tmp/1234_photo.png": "/media/md-editor/uploads/2026/03/1234_photo.png"}}`

    Called automatically by the editor on form submit.

## Template Tags & Filters

Load with `{% load markdown_widget %}`.

### `{% markdown text %}`

:   Render markdown text as sanitized HTML (simple tag).

### `{{ text|markdown }}`

:   Render markdown text as sanitized HTML (filter).
