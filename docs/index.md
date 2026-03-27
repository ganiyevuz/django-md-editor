# django-md-editor

A GitHub-style markdown editor widget for Django forms and admin.

## Why django-md-editor?

- **Drop-in widget** -- works with any Django form or ModelForm
- **One-line admin integration** -- mixin replaces TextFields with the editor
- **Pluggable architecture** -- swap renderers and upload handlers without changing code
- **No heavy dependencies** -- only Django is required; markdown library is optional
- **Themes** -- light, dark, and auto (follows system preference)

## Quick Example

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

That's it. The editor includes a toolbar, live preview, image uploads, and keyboard shortcuts out of the box.

## Next Steps

- [Installation](getting-started/installation.md) -- install the package and wire it up
- [Quick Start](getting-started/quickstart.md) -- form, admin, and template usage in 5 minutes
- [Configuration](guide/configuration.md) -- all available settings
