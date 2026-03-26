from django.template import Context, Template
from django.test import TestCase


class MarkdownTagTests(TestCase):
    def test_renders_markdown_text(self):
        template = Template("{% load md_editor %}{% markdown content %}")
        context = Context({"content": "**bold**"})
        result = template.render(context)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_renders_empty_string(self):
        template = Template("{% load md_editor %}{% markdown content %}")
        context = Context({"content": ""})
        result = template.render(context)
        assert result.strip() == ""

    def test_renders_none_as_empty(self):
        template = Template("{% load md_editor %}{% markdown content %}")
        context = Context({"content": None})
        result = template.render(context)
        assert result.strip() == ""

    def test_escapes_html_in_fallback(self):
        template = Template("{% load md_editor %}{% markdown content %}")
        context = Context({"content": "<script>alert('xss')</script>"})
        result = template.render(context)
        assert "<script>" not in result
