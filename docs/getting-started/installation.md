# Installation

## Requirements

- Python 3.11+
- Django 5.2+

## Install the Package

```bash
pip install django-markdown-widget
```

## Add to Django Settings

```python
INSTALLED_APPS = [
    ...
    "django_markdown_widget",
]
```

## Include URLs

The editor needs two endpoints: one for server-side preview and one for file uploads.

```python
# urls.py
from django.urls import include, path

urlpatterns = [
    ...
    path("md-editor/", include("django_markdown_widget.urls")),
]
```

## Optional: Install a Markdown Library

The default renderer uses [python-markdown](https://python-markdown.github.io/) for server-side rendering. If it's not installed, the renderer falls back to escaped plaintext.

```bash
pip install markdown
```

!!! note
    Client-side preview always works -- it uses the bundled [marked.js](https://marked.js.org/) library. The server-side renderer is used by the `{% markdown %}` template tag and the preview API endpoint.

## Verify

Start your development server and add a `MarkdownEditorWidget` to any form. You should see the editor with a toolbar, write/preview tabs, and a footer.
