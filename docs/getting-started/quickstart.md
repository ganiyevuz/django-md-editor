# Quick Start

This guide covers the three most common use cases: forms, admin, and templates.

## Form Widget

Replace Django's default `Textarea` with `MarkdownEditorWidget`:

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

The widget accepts optional parameters:

```python
MarkdownEditorWidget(
    toolbar=["bold", "italic", "link"],  # custom toolbar
    height="500px",                       # editor height
    placeholder="Write something...",     # placeholder text
    preview_url="/md-editor/preview",    # server preview endpoint
    upload_url="/md-editor/upload",      # file upload endpoint
)
```

## Django Admin

Use `MarkdownEditorAdminMixin` to replace TextFields in the admin:

```python
from django.contrib import admin
from django_md_editor import MarkdownEditorAdminMixin

@admin.register(Post)
class PostAdmin(MarkdownEditorAdminMixin, admin.ModelAdmin):
    list_display = ["title", "created_at"]
```

By default, all TextFields get the editor. To limit to specific fields:

```python
class PostAdmin(MarkdownEditorAdminMixin, admin.ModelAdmin):
    markdown_fields = ["content"]  # only "content" gets the editor
```

## Template Rendering

Load the template tag library and render markdown content:

```django
{% load md_editor %}

{# As a filter (recommended) #}
{{ post.content|markdown }}

{# As a tag #}
{% markdown post.content %}
```

Both produce the same output -- the filter syntax is more idiomatic in Django templates.
