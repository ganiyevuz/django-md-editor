# Themes

The editor supports three theme modes: light, dark, and auto.

## Configuration

Set the theme globally:

```python
MD_EDITOR = {
    "THEME": "auto",  # "light", "dark", or "auto"
}
```

## Theme Modes

### `"auto"` (default)

Follows the user's system color scheme preference using `prefers-color-scheme` media query. The editor automatically switches between light and dark as the OS setting changes.

### `"light"`

Forces the light theme regardless of system preference. White background with dark text.

### `"dark"`

Forces the dark theme regardless of system preference. Dark background with light text.

## CSS Custom Properties

The editor uses CSS custom properties for theming. You can override these in your own stylesheet to customize colors:

```css
.md-editor {
    --md-bg: #ffffff;
    --md-text: #1f2328;
    --md-border: #d1d9e0;
    --md-toolbar-bg: #f6f8fa;
    --md-input-bg: #ffffff;
    --md-preview-bg: #ffffff;
    --md-btn-hover: #e0e4e8;
    --md-accent: #0969da;
    --md-placeholder: #59636e;
    --md-footer-bg: #f6f8fa;
    --md-tab-active: #1f2328;
    --md-tab-inactive: #59636e;
    --md-focus-ring: rgba(9, 105, 218, 0.3);
}
```

For dark mode, target the `.md-editor--dark` class:

```css
.md-editor--dark {
    --md-bg: #0d1117;
    --md-text: #e6edf3;
    /* ... */
}
```
