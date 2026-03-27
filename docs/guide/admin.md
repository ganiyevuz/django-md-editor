# Admin Integration

`MarkdownEditorAdminMixin` provides one-line integration with the Django admin.

## All TextFields

Add the mixin to your `ModelAdmin` to replace **all** TextFields with the markdown editor:

```python
from django.contrib import admin
from django_md_editor import MarkdownEditorAdminMixin

@admin.register(Post)
class PostAdmin(MarkdownEditorAdminMixin, admin.ModelAdmin):
    list_display = ["title", "created_at"]
```

## Specific Fields Only

Use `markdown_fields` to limit which fields get the editor:

```python
@admin.register(Post)
class PostAdmin(MarkdownEditorAdminMixin, admin.ModelAdmin):
    list_display = ["title", "created_at"]
    markdown_fields = ["content"]  # "summary" stays as a regular textarea
```

## How It Works

When `markdown_fields` is `None` (the default), the mixin adds `MarkdownEditorWidget` to `formfield_overrides` for all `TextField` instances.

When `markdown_fields` is a list, it overrides `formfield_for_dbfield()` to selectively apply the widget only to the named fields.

!!! tip
    The mixin must come **before** `admin.ModelAdmin` in the class inheritance order so its methods take precedence.
