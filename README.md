# django-md-editor

A GitHub-style markdown editor widget for Django forms and admin.

[![PyPI version](https://img.shields.io/pypi/v/django-markdown-widget.svg)](https://pypi.org/project/django-markdown-widget/)
[![Python versions](https://img.shields.io/pypi/pyversions/django-markdown-widget.svg)](https://pypi.org/project/django-markdown-widget/)
[![Django versions](https://img.shields.io/badge/django-5.2%2B-blue.svg)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Docs](https://img.shields.io/badge/docs-mkdocs-blue.svg)](https://ganiyevuz.github.io/django-md-editor/)

**[Documentation](https://ganiyevuz.github.io/django-md-editor/)** | **[PyPI](https://pypi.org/project/django-markdown-widget/)** | **[GitHub](https://github.com/ganiyevuz/django-md-editor)**

## Features

- GitHub-flavored markdown editor with live preview
- Toolbar with common formatting actions (headings, bold, italic, code, tables, etc.)
- Image and file uploads with drag & drop support
- Light, dark, and auto theme support
- Django admin integration via one-line mixin
- Template tag and filter for rendering markdown in templates
- Pluggable renderer and upload handler architecture
- Automatic media cleanup for orphaned uploads
- Management command for bulk orphan detection
- Zero hard dependencies beyond Django (markdown library is optional)
- Keyboard shortcuts (Ctrl+B, Ctrl+I, Ctrl+K, etc.)

## Installation

```bash
pip install django-markdown-widget
```

Add to your `INSTALLED_APPS` and include the URLs:

```python
# settings.py
INSTALLED_APPS = [
    ...
    "django_md_editor",
]

# urls.py
from django.urls import include, path

urlpatterns = [
    ...
    path("md-editor/", include("django_md_editor.urls")),
]
```

For server-side rendering, install a markdown library:

```bash
pip install markdown
```

## Quick Start

### Form Widget

```python
from django.forms import ModelForm
from django_md_editor import MarkdownEditorWidget

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
from django_md_editor import MarkdownEditorAdminMixin

@admin.register(Post)
class PostAdmin(MarkdownEditorAdminMixin, admin.ModelAdmin):
    list_display = ["title", "created_at"]
    markdown_fields = ["content"]  # omit to apply to all TextFields
```

### Template Rendering

```django
{% load md_editor %}

{# As a filter (recommended) #}
{{ post.content|markdown }}

{# As a tag #}
{% markdown post.content %}
```

### Media Cleanup

```python
from django_md_editor import MarkdownCleanupMixin

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

## Configuration

All settings are optional and go under `MD_EDITOR` in your Django settings:

```python
MD_EDITOR = {
    # Pluggable backend classes
    "RENDERER_CLASS": "django_md_editor.renderers.DefaultRenderer",
    "UPLOAD_HANDLER_CLASS": "django_md_editor.uploads.DefaultUploadHandler",

    # Toolbar buttons
    "TOOLBAR": [
        "heading", "bold", "italic", "strikethrough", "separator",
        "quote", "code", "code-block", "link", "image", "separator",
        "ordered-list", "unordered-list", "task-list", "separator",
        "horizontal-rule", "table", "details", "separator",
        "highlight", "superscript", "subscript", "separator",
        "attach", "mention", "ref", "separator",
        "undo", "redo", "fullscreen",
    ],

    # Upload settings
    "ALLOWED_UPLOAD_TYPES": ["image/png", "image/jpeg", "image/gif", "image/webp"],
    "MAX_UPLOAD_SIZE": 10 * 1024 * 1024,  # 10 MB
    "UPLOAD_PATH": "md-editor/uploads/%Y/%m/",

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
from django_md_editor import BaseRenderer

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
from django_md_editor import BaseUploadHandler

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
