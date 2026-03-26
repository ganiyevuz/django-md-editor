from django.test import TestCase

from django_md_editor.renderers import BaseRenderer, DefaultRenderer


class BaseRendererTests(TestCase):
    def test_render_raises_not_implemented(self):
        renderer = BaseRenderer()
        with self.assertRaises(NotImplementedError):
            renderer.render("some text")


class DefaultRendererTests(TestCase):
    def test_renders_plain_text_when_no_library_installed(self):
        renderer = DefaultRenderer()
        result = renderer.render("**bold text**")
        assert isinstance(result, str)

    def test_renders_empty_string(self):
        renderer = DefaultRenderer()
        result = renderer.render("")
        assert result == ""

    def test_escapes_html_in_fallback_mode(self):
        renderer = DefaultRenderer()
        result = renderer.render("<script>alert('xss')</script>")
        assert "<script>" not in result
        assert "&lt;script&gt;" in result
