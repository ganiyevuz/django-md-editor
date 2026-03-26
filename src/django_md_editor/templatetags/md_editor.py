from django import template
from django.utils.module_loading import import_string
from django.utils.safestring import mark_safe

from django_md_editor.settings import get_setting

register = template.Library()


@register.simple_tag
def markdown(text):
    if not text:
        return ""
    renderer_class = import_string(get_setting("RENDERER_CLASS"))
    renderer = renderer_class()
    return mark_safe(renderer.render(text))
