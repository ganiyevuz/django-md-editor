# Toolbar Customization

The toolbar is configured as a list of button names. You can customize it globally via settings or per widget instance.

## Available Buttons

| Button | Description |
|--------|-------------|
| `bold` | Bold text |
| `italic` | Italic text |
| `strikethrough` | Strikethrough text |
| `highlight` | Highlighted text (`==text==`) |
| `heading` | Cycling heading (H1 > H2 > H3 > paragraph) |
| `quote` | Blockquote |
| `horizontal-rule` | Horizontal rule (`---`) |
| `code` | Inline code |
| `code-block` | Fenced code block |
| `unordered-list` | Bullet list |
| `ordered-list` | Numbered list |
| `task-list` | Checkbox list |
| `link` | Hyperlink |
| `image` | Image (opens file picker for images) |
| `video` | Video (opens file picker for videos) |
| `document` | Document (opens file picker for documents) |
| `table` | Table |
| `details` | Collapsible details/summary block |
| `embed` | Embed (YouTube, Vimeo, CodePen, or raw iframe) |
| `superscript` | Superscript (`^text^`) |
| `subscript` | Subscript (`~text~`) |
| `attach` | Generic file attachment (any file type) |
| `undo` | Undo |
| `redo` | Redo |
| `fullscreen` | Toggle fullscreen (also available in tabs bar) |
| `separator` | Visual divider between button groups |

## Default Toolbar

Grouped by purpose:

```python
"TOOLBAR": [
    # Text formatting
    "bold", "italic", "strikethrough", "highlight",
    "separator",
    # Headings & structure
    "heading", "quote", "horizontal-rule",
    "separator",
    # Code
    "code", "code-block",
    "separator",
    # Lists
    "unordered-list", "ordered-list", "task-list",
    "separator",
    # Links & media
    "link", "image", "video", "document",
    "separator",
    # Rich blocks
    "table", "details", "embed",
    "separator",
    # Extras
    "superscript", "subscript",
    "separator",
    # Actions (right-aligned)
    "undo", "redo",
]
```

## Per-Widget Configuration

```python
MarkdownEditorWidget(
    toolbar=["bold", "italic", "link", "image"],
)
```

The per-widget toolbar overrides the global setting for that specific widget instance.

## Minimal Toolbar

```python
MarkdownEditorWidget(toolbar=["bold", "italic", "link"])
```

## Comment-Style Toolbar

```python
MarkdownEditorWidget(
    toolbar=[
        "bold", "italic", "strikethrough", "separator",
        "link", "code", "quote", "separator",
        "unordered-list", "task-list",
    ],
    height="150px",
    placeholder="Leave a comment...",
)
```

## Full-Featured Toolbar

```python
MarkdownEditorWidget(
    toolbar=[
        "bold", "italic", "strikethrough", "highlight", "separator",
        "heading", "quote", "horizontal-rule", "separator",
        "code", "code-block", "separator",
        "unordered-list", "ordered-list", "task-list", "separator",
        "link", "image", "video", "document", "separator",
        "table", "details", "embed", "separator",
        "superscript", "subscript", "separator",
        "undo", "redo",
    ],
)
```

## Header Controls

These are always present in the tabs bar (not configurable via toolbar):

- **Autosave toggle** -- switch to enable/disable draft saving
- **Fullscreen button** -- expands editor to fill the viewport
