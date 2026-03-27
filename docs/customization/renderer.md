# Custom Renderer

The renderer converts markdown text to HTML on the server side. It's used by the template tag/filter and the preview API endpoint.

## Default Renderer

`DefaultRenderer` uses [python-markdown](https://python-markdown.github.io/) with the `extra`, `codehilite`, and `toc` extensions. If python-markdown is not installed, it falls back to HTML-escaped plaintext.

## Creating a Custom Renderer

Subclass `BaseRenderer` and implement the `render` method:

```python
from django_md_editor import BaseRenderer

class MarkdownItRenderer(BaseRenderer):
    def render(self, markdown_text: str) -> str:
        if not markdown_text:
            return ""
        import markdown_it
        md = markdown_it.MarkdownIt()
        return md.render(markdown_text)
```

### With Sanitization

For user-generated content, sanitize the output:

```python
import nh3
from django_md_editor import BaseRenderer

class SafeRenderer(BaseRenderer):
    def render(self, markdown_text: str) -> str:
        if not markdown_text:
            return ""
        import markdown
        html = markdown.markdown(markdown_text, extensions=["extra"])
        return nh3.clean(html)
```

## Register Your Renderer

```python
MD_EDITOR = {
    "RENDERER_CLASS": "myapp.renderers.MarkdownItRenderer",
}
```

The class is loaded via `django.utils.module_loading.import_string`, so any importable Python path works.
