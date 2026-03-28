# django-markdown-widget

A GitHub-style markdown editor widget for Django forms and admin.

[![PyPI version](https://img.shields.io/pypi/v/django-markdown-widget.svg)](https://pypi.org/project/django-markdown-widget/)
[![Python versions](https://img.shields.io/pypi/pyversions/django-markdown-widget.svg)](https://pypi.org/project/django-markdown-widget/)
[![Django versions](https://img.shields.io/badge/django-5.2%2B-blue.svg)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![codecov](https://codecov.io/gh/ganiyevuz/django-md-editor/graph/badge.svg)](https://codecov.io/gh/ganiyevuz/django-md-editor)
[![Docs](https://img.shields.io/badge/docs-mkdocs-blue.svg)](https://ganiyevuz.github.io/django-md-editor/)

**[Documentation](https://ganiyevuz.github.io/django-md-editor/)** | **[PyPI](https://pypi.org/project/django-markdown-widget/)** | **[GitHub](https://github.com/ganiyevuz/django-md-editor)**

## Screenshots

| Dark (default) | Light |
|:-:|:-:|
| ![Write](https://raw.githubusercontent.com/ganiyevuz/django-md-editor/main/docs/screenshots/editor-write.png) | ![Light](https://raw.githubusercontent.com/ganiyevuz/django-md-editor/main/docs/screenshots/editor-light.png) |

| Split View | Preview |
|:-:|:-:|
| ![Split](https://raw.githubusercontent.com/ganiyevuz/django-md-editor/main/docs/screenshots/editor-split.png) | ![Preview](https://raw.githubusercontent.com/ganiyevuz/django-md-editor/main/docs/screenshots/editor-preview.png) |

## Features

- **Three view modes** -- Write, Split (side-by-side live preview), Preview
- **Syntax highlighting** for code blocks via highlight.js (GitHub themes)
- **Rich toolbar** -- text formatting, headings, lists, code, tables, media, embeds
- **Image, video, and document uploads** with drag & drop support
- **Embed support** -- paste YouTube, Vimeo, CodePen URLs or raw `<iframe>` code
- **Autosave** -- drafts saved to browser localStorage, survives page reloads
- **Draggable split divider** -- resize editor/preview panels
- **Temp upload system** -- files upload to temp storage, finalize on form submit
- **Light, dark, and auto** theme support
- **Django admin integration** via one-line mixin
- **Template tag and filter** for server-side markdown rendering
- **Pluggable renderer and upload handler** architecture
- **Media cleanup** -- automatic orphaned file deletion + management command
- **Custom undo/redo** history stack (100 states)
- **HTML sanitization** on both client and server side
- **Keyboard shortcuts** -- Ctrl+B, Ctrl+I, Ctrl+K, Ctrl+Z, etc.
- **Zero hard dependencies** beyond Django

## Installation

```bash
pip install django-markdown-widget
```

Add to your `INSTALLED_APPS` and include the URLs:

```python
# settings.py
INSTALLED_APPS = [
    ...
    "django_markdown_widget",
]

# urls.py
from django.urls import include, path

urlpatterns = [
    ...
    path("md-editor/", include("django_markdown_widget.urls")),
]
```

For server-side rendering (template tag/filter), install a markdown library:

```bash
pip install markdown
```

## Quick Start

### Form Widget

```python
from django.forms import ModelForm
from django_markdown_widget import MarkdownEditorWidget

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]
        widgets = {
            "content": MarkdownEditorWidget(),
        }
```

### Django Admin

```python
from django.contrib import admin
from django_markdown_widget import MarkdownEditorAdminMixin

@admin.register(Post)
class PostAdmin(MarkdownEditorAdminMixin, admin.ModelAdmin):
    list_display = ["title", "created_at"]
    markdown_fields = ["content"]  # omit to apply to all TextFields
```

### Template Rendering

```django
{% load markdown_widget %}

{# As a filter (recommended) #}
{{ post.content|markdown }}

{# As a tag #}
{% markdown post.content %}
```

### Media Cleanup

```python
from django_markdown_widget import MarkdownCleanupMixin

class Post(MarkdownCleanupMixin, models.Model):
    content = models.TextField()
    # markdown_cleanup_fields = ["content"]  # optional: limit to specific fields
```

Enable in settings:

```python
MD_EDITOR = {
    "CLEANUP_MEDIA": True,
}
```

Bulk cleanup via management command:

```bash
python manage.py cleanup_markdown_media --dry-run
python manage.py cleanup_markdown_media
```

## Toolbar

Default toolbar layout, grouped by purpose:

| Group | Buttons |
|-------|---------|
| Text formatting | Bold, Italic, Strikethrough, Highlight |
| Structure | Heading, Quote, Horizontal rule |
| Code | Inline code, Code block |
| Lists | Bullet, Numbered, Task list |
| Links & media | Link, Image, Video, Document |
| Rich blocks | Table, Collapsible section, Embed |
| Extras | Superscript, Subscript |
| Actions | Undo, Redo |

Fullscreen toggle and autosave switch are in the top-right tabs bar.

## Configuration

All settings are optional and go under `MD_EDITOR` in your Django settings:

```python
MD_EDITOR = {
    # Pluggable backend classes
    "RENDERER_CLASS": "django_markdown_widget.renderers.DefaultRenderer",
    "UPLOAD_HANDLER_CLASS": "django_markdown_widget.uploads.DefaultUploadHandler",

    # Toolbar buttons (grouped by purpose)
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

    # Upload settings
    "ALLOWED_UPLOAD_TYPES": [
        "image/png", "image/jpeg", "image/gif", "image/webp",
        "video/mp4", "video/webm", "video/ogg",
        "application/pdf", "application/zip", "text/plain", "text/csv",
        "application/json",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ],
    "MAX_UPLOAD_SIZE": 50 * 1024 * 1024,  # 50 MB
    "UPLOAD_PATH": "md-editor/uploads/%Y/%m/",
    "TEMP_UPLOAD_PATH": "md-editor/tmp/",
    "TEMP_MAX_AGE": 86400,  # 24 hours

    # Editor defaults
    "DEFAULT_HEIGHT": "300px",
    "PLACEHOLDER": "Add your comment here...",
    "THEME": "auto",  # "light", "dark", or "auto"

    # Security
    "REQUIRE_AUTH": True,

    # Media cleanup
    "CLEANUP_MEDIA": False,
}
```

## Custom Renderer

```python
from django_markdown_widget import BaseRenderer

class MyRenderer(BaseRenderer):
    def render(self, markdown_text: str) -> str:
        import markdown_it
        md = markdown_it.MarkdownIt()
        return md.render(markdown_text)
```

```python
MD_EDITOR = {
    "RENDERER_CLASS": "myapp.renderers.MyRenderer",
}
```

## Custom Upload Handler

```python
from django_markdown_widget import BaseUploadHandler

class S3UploadHandler(BaseUploadHandler):
    def validate(self, file):
        # your validation logic
        pass

    def save(self, file) -> str:
        # save to S3 and return the URL
        return url
```

```python
MD_EDITOR = {
    "UPLOAD_HANDLER_CLASS": "myapp.uploads.S3UploadHandler",
}
```

## Development

```bash
git clone https://github.com/ganiyevuz/django-md-editor.git
cd django-md-editor
uv sync --group dev
make test
make lint
```

Run the example app:

```bash
cd example
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## License

MIT License. See [LICENSE](LICENSE) for details.
