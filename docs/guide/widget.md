# Widget

`MarkdownEditorWidget` is a Django form widget that replaces the standard `<textarea>` with a full markdown editor.

## Basic Usage

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

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `toolbar` | `list[str]` | from settings | List of toolbar button names |
| `upload_url` | `str` | `"/md-editor/upload"` | File upload endpoint |
| `finalize_url` | `str` | `"/md-editor/finalize"` | Finalize temp uploads endpoint |
| `height` | `str` | `"300px"` | CSS height of the editor |
| `placeholder` | `str` | `"Add your comment here..."` | Placeholder text |
| `attrs` | `dict` | `None` | Extra HTML attributes for the textarea |

## View Modes

The editor has three tabs:

| Mode | Description |
|------|-------------|
| **Write** | Editor only with toolbar |
| **Split** | Side-by-side editor and live preview -- updates as you type |
| **Preview** | Rendered output only, toolbar hidden |

The split view has a **draggable divider** to resize the editor and preview panels (20% to 80%).

Code blocks in the preview are syntax-highlighted via [highlight.js](https://highlightjs.org/) with GitHub-style colors that adapt to the current theme.

## Toolbar

Default toolbar grouped by purpose:

| Group | Buttons |
|-------|---------|
| Text formatting | Bold, Italic, Strikethrough, Highlight |
| Structure | Heading, Quote, Horizontal rule |
| Code | Inline code, Code block |
| Lists | Bullet, Numbered, Task list |
| Links & media | Link, Image, Video, Document |
| Rich blocks | Table, Collapsible section, Embed |
| Extras | Superscript, Subscript |
| Actions (right) | Undo, Redo |

Fullscreen toggle and autosave switch are in the top-right tabs bar.

### Custom Toolbar Per Widget

```python
MarkdownEditorWidget(
    toolbar=["bold", "italic", "separator", "link", "image"],
)
```

## Uploads

The editor supports three media types:

| Type | Toolbar button | Inserted as |
|------|---------------|-------------|
| Image | Image button | `![name](url)` |
| Video | Video button | `<video>` with controls |
| Document | Document button | `[name](url)` (download link) |

Files upload to temp storage (`md-editor/tmp/`) first. On form submit, referenced files are moved to permanent storage automatically.

## Embeds

The Embed button accepts:

- **YouTube URL** -- `https://www.youtube.com/watch?v=ID` -- generates `<iframe>` embed
- **Vimeo URL** -- `https://vimeo.com/ID`
- **CodePen URL** -- `https://codepen.io/user/pen/ID`
- **Raw `<iframe>` code** -- paste YouTube's embed code directly
- **Any URL** -- generic iframe embed

## Autosave

Drafts are automatically saved to browser `localStorage` as you type:

- Debounced (500ms after you stop typing)
- Toggle on/off via the switch in the tabs bar
- Footer shows "Saving...", "Saved at 2:31 PM"
- Restores draft on page load if textarea is empty
- Clears on form submit; expires after 7 days

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+B` | Bold |
| `Ctrl+I` | Italic |
| `Ctrl+K` | Link |
| `Ctrl+E` | Code |
| `Ctrl+Shift+.` | Quote |
| `Ctrl+Shift+7` | Ordered list |
| `Ctrl+Shift+8` | Unordered list |
| `Ctrl+Z` | Undo |
| `Ctrl+Shift+Z` | Redo |
| `Escape` | Exit fullscreen |

## Multiple Editors on One Page

Each editor instance is independent:

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

## Media Assets

The widget automatically includes its CSS and JavaScript via Django's `Media` framework:

- `django_markdown_widget/css/editor.css`
- `django_markdown_widget/js/markdown-it.min.js` (client-side markdown rendering)
- `django_markdown_widget/js/markdown-it-mark.min.js` (highlight syntax)
- `django_markdown_widget/js/markdown-it-sub.min.js` (subscript)
- `django_markdown_widget/js/markdown-it-sup.min.js` (superscript)
- `django_markdown_widget/js/markdown-it-task-lists.min.js` (checkboxes)
- `django_markdown_widget/js/highlight.min.js` (syntax highlighting)
- `django_markdown_widget/js/editor.js`

These are served from Django's static files. Make sure `django.contrib.staticfiles` is in your `INSTALLED_APPS` or that you collect static files for production.
