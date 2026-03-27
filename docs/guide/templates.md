# Template Rendering

Render stored markdown content as HTML in your templates.

## Setup

Load the `md_editor` template tag library:

```django
{% load markdown_widget %}
```

## Filter (Recommended)

```django
<article>
  {{ post.content|markdown }}
</article>
```

## Tag

```django
<article>
  {% markdown post.content %}
</article>
```

Both produce the same output. The filter syntax is more idiomatic in Django.

## How It Works

The template tag/filter:

1. Loads the renderer class from `MD_EDITOR["RENDERER_CLASS"]`
2. Calls `renderer.render(text)` to convert markdown to HTML
3. Marks the output as safe (`mark_safe`)

!!! warning
    The output is marked as safe, so make sure your renderer sanitizes HTML if you accept user input. The `DefaultRenderer` uses python-markdown which does not sanitize by default. Consider using [bleach](https://github.com/mozilla/bleach) or [nh3](https://github.com/messense/nh3) in a custom renderer for user-generated content.

## Empty Content

Both the filter and tag return an empty string for `None` or `""` values, so no special handling is needed in templates.
