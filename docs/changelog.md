# Changelog

## 1.0.1

- Modernized base classes with `abc.ABC` and `@abstractmethod`
- Added `from __future__ import annotations` across all modules
- DRYed up view auth check into `AuthRequiredMixin`
- Catch `ValidationError` specifically instead of bare `Exception` in upload view
- Added `markdown` template filter (`{{ text|markdown }}`) alongside existing tag
- Added `MarkdownCleanupMixin` for automatic orphaned media deletion on model save
- Added `cleanup_markdown_media` management command for bulk orphan detection
- Added `extract_media_urls()` and `delete_orphaned_media()` utility functions
- Added `CLEANUP_MEDIA` setting (opt-in, defaults to `False`)
- Added type hints for upload handler methods (`UploadedFile`)
- Added return type hint for `get_setting()`
- Removed deprecated `default_app_config` (unnecessary since Django 3.2)
- Added mkdocs documentation site with Material theme
- Updated README with full usage guide
- Test coverage at 95%+ (82 tests)

## 1.0.0

Initial release.

- GitHub-style markdown editor widget for Django forms
- Django admin integration via `MarkdownEditorAdminMixin`
- Pluggable renderer and upload handler architecture
- `DefaultRenderer` with python-markdown (optional dependency)
- `DefaultUploadHandler` with Django's `default_storage`
- Template tag (`{% markdown %}`) for rendering markdown in templates
- Image/file upload with drag & drop and paste support
- Toolbar with headings, formatting, lists, tables, code blocks, and more
- Light, dark, and auto theme support
- Keyboard shortcuts (Ctrl+B, Ctrl+I, Ctrl+K, etc.)
- Full test suite with pytest
