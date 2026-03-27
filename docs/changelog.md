# Changelog

## 1.0.0 (Unreleased)

Initial release.

- GitHub-style markdown editor widget for Django forms
- Django admin integration via `MarkdownEditorAdminMixin`
- Pluggable renderer and upload handler architecture
- `DefaultRenderer` with python-markdown (optional dependency)
- `DefaultUploadHandler` with Django's `default_storage`
- Template tag (`{% markdown %}`) and filter (`{{ text|markdown }}`)
- Image/file upload with drag & drop and paste support
- Toolbar with headings, formatting, lists, tables, code blocks, and more
- Light, dark, and auto theme support
- Keyboard shortcuts (Ctrl+B, Ctrl+I, Ctrl+K, etc.)
- `MarkdownCleanupMixin` for automatic orphaned media deletion
- `cleanup_markdown_media` management command for bulk cleanup
- Full test suite with 95%+ coverage
