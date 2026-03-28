# Welcome to Django Markdown Widget

A **GitHub-style** markdown editor for Django forms and admin.

## Features

- **Live preview** with instant client-side rendering
- **Split view** — write and preview side by side
- ~~Old textarea~~ replaced with a modern editor
- Supports `inline code` and fenced blocks
- **Syntax highlighting** powered by highlight.js
- **Light, dark, and auto** theme support
- **Drag & drop** image uploads
- **Keyboard shortcuts** — Ctrl+B, Ctrl+I, Ctrl+K, and more

## Quick Example

```python
from django.forms import ModelForm
from django_markdown_widget import MarkdownEditorWidget

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]
        widgets = {"content": MarkdownEditorWidget()}
```

### Admin Integration

```python
from django.contrib import admin
from django_markdown_widget import MarkdownEditorAdminMixin

@admin.register(Post)
class PostAdmin(MarkdownEditorAdminMixin, admin.ModelAdmin):
    list_display = ["title", "created_at"]
    markdown_fields = ["content"]
```

### Template Rendering

```django
{% load markdown_widget %}

{{ post.content|markdown }}
```

### Media Cleanup

```python
from django_markdown_widget import MarkdownCleanupMixin

class Post(MarkdownCleanupMixin, models.Model):
    content = models.TextField()
    markdown_cleanup_fields = ["content"]
```

## Task List

- [x] Installation
- [x] Admin integration
- [x] Split preview mode
- [x] Syntax highlighting
- [x] Media cleanup
- [ ] Custom renderer
- [ ] Deploy to production

## Comparison

| Feature          | Textarea | Markdown Widget |
|------------------|----------|-----------------|
| Live preview     | No       | Yes             |
| Split view       | No       | Yes             |
| Toolbar          | No       | Yes             |
| File uploads     | No       | Yes             |
| Syntax highlight | No       | Yes             |
| Themes           | No       | Light/Dark/Auto |
| Keyboard shortcuts | No     | Yes             |

## Configuration

```python
MD_EDITOR = {
    "TOOLBAR": ["heading", "bold", "italic", "code", "link", "image"],
    "THEME": "auto",
    "UPLOAD_PATH": "md-editor/uploads/%Y/%m/",
    "MAX_UPLOAD_SIZE": 10 * 1024 * 1024,
    "CLEANUP_MEDIA": True,
}
```

> **Drop-in** replacement for any Django `TextField` — works in **forms and admin** with zero configuration.

---

Powered by [django-markdown-widget](https://github.com/ganiyevuz/django-md-editor)
