# Widget

`MarkdownEditorWidget` is a Django form widget that replaces the standard `<textarea>` with a full markdown editor.

## Basic Usage

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

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `toolbar` | `list[str]` | from settings | List of toolbar button names |
| `height` | `str` | `"300px"` | CSS height of the editor |
| `placeholder` | `str` | `"Add your comment here..."` | Placeholder text |
| `preview_url` | `str` | `"/md-editor/preview"` | Server-side preview endpoint |
| `upload_url` | `str` | `"/md-editor/upload"` | File upload endpoint |
| `attrs` | `dict` | `None` | Extra HTML attributes for the textarea |

## Custom Toolbar Per Widget

```python
MarkdownEditorWidget(
    toolbar=["bold", "italic", "separator", "link", "image"],
)
```

## Multiple Editors on One Page

Each editor instance is independent. You can have multiple editors with different configurations on the same page:

```python
class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ["summary", "body"]
        widgets = {
            "summary": MarkdownEditorWidget(
                height="150px",
                toolbar=["bold", "italic", "link"],
            ),
            "body": MarkdownEditorWidget(
                height="500px",
            ),
        }
```

## Keyboard Shortcuts

The editor supports these keyboard shortcuts:

| Shortcut | Action |
|----------|--------|
| `Ctrl+B` | Bold |
| `Ctrl+I` | Italic |
| `Ctrl+K` | Link |
| `Ctrl+Shift+X` | Strikethrough |
| `Ctrl+Z` | Undo |
| `Ctrl+Shift+Z` | Redo |
| `Tab` | Indent |
| `Shift+Tab` | Outdent |

## Media Assets

The widget automatically includes its CSS and JavaScript via Django's `Media` framework:

- `django_md_editor/css/editor.css`
- `django_md_editor/js/marked.min.js`
- `django_md_editor/js/editor.js`

These are served from Django's static files. Make sure `django.contrib.staticfiles` is in your `INSTALLED_APPS` or that you collect static files for production.
