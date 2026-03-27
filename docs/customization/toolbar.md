# Toolbar Customization

The toolbar is configured as a list of button names. You can customize it globally via settings or per widget instance.

## Available Buttons

| Button | Description |
|--------|-------------|
| `heading` | Cycling heading (H1 > H2 > H3 > paragraph) |
| `bold` | Bold text |
| `italic` | Italic text |
| `strikethrough` | Strikethrough text |
| `quote` | Blockquote |
| `code` | Inline code |
| `code-block` | Fenced code block |
| `link` | Hyperlink |
| `image` | Image |
| `ordered-list` | Numbered list |
| `unordered-list` | Bullet list |
| `task-list` | Checkbox list |
| `horizontal-rule` | Horizontal rule (`---`) |
| `table` | Table |
| `details` | Collapsible details/summary block |
| `highlight` | Highlighted text (`==text==`) |
| `superscript` | Superscript (`^text^`) |
| `subscript` | Subscript (`~text~`) |
| `attach` | File attachment |
| `mention` | Mention (`@username`) |
| `ref` | Reference (`#123`) |
| `undo` | Undo |
| `redo` | Redo |
| `fullscreen` | Toggle fullscreen |
| `separator` | Visual divider between button groups |

## Global Configuration

```python
MD_EDITOR = {
    "TOOLBAR": [
        "heading", "bold", "italic", "separator",
        "link", "image", "code", "separator",
        "unordered-list", "ordered-list", "separator",
        "undo", "redo", "fullscreen",
    ],
}
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
