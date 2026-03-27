from __future__ import annotations

from django import template
from django.utils.module_loading import import_string
from django.utils.safestring import mark_safe

from django_md_editor.settings import get_setting

register = template.Library()


def _render_markdown(text: str) -> str:
    if not text:
        return ""
    renderer_class = import_string(get_setting("RENDERER_CLASS"))
    renderer = renderer_class()
    return renderer.render(text)


@register.simple_tag
def markdown(text: str) -> str:
    return mark_safe(_render_markdown(text))


@register.filter(name="markdown")
def markdown_filter(text: str) -> str:
    return mark_safe(_render_markdown(text))
