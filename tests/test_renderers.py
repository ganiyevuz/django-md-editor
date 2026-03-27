from unittest.mock import patch

from django.test import TestCase

from django_md_editor.renderers import BaseRenderer, DefaultRenderer


class BaseRendererTests(TestCase):
    def test_cannot_instantiate_abstract_class(self):
        with self.assertRaises(TypeError):
            BaseRenderer()


class DefaultRendererTests(TestCase):
    def test_renders_plain_text_when_no_library_installed(self):
        renderer = DefaultRenderer()
        result = renderer.render("**bold text**")
        assert isinstance(result, str)

    def test_renders_empty_string(self):
        renderer = DefaultRenderer()
        result = renderer.render("")
        assert result == ""

    @patch.dict("sys.modules", {"markdown": None})
    def test_escapes_html_in_fallback_mode(self):
        renderer = DefaultRenderer()
        result = renderer.render("<script>alert('xss')</script>")
        assert "<script>" not in result
        assert "&lt;script&gt;" in result

    @patch.dict("sys.modules", {"markdown": None})
    def test_falls_back_to_escaped_text_when_markdown_unavailable(self):
        renderer = DefaultRenderer()
        result = renderer.render("**bold**")
        assert result == "**bold**"
