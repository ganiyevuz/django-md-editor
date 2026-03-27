from django.test import TestCase

from django_markdown_widget.widgets import MarkdownEditorWidget


class MarkdownEditorWidgetTests(TestCase):
    def test_default_attrs(self):
        widget = MarkdownEditorWidget()
        assert widget.template_name == "django_markdown_widget/widget.html"

    def test_media_includes_css(self):
        widget = MarkdownEditorWidget()
        css = str(widget.media)
        assert "django_markdown_widget/css/editor.css" in css

    def test_media_includes_js(self):
        widget = MarkdownEditorWidget()
        js = str(widget.media)
        assert "django_markdown_widget/js/editor.js" in js
        assert "django_markdown_widget/js/marked.min.js" in js

    def test_custom_toolbar(self):
        toolbar = ["bold", "italic"]
        widget = MarkdownEditorWidget(toolbar=toolbar)
        ctx = widget.get_context("content", "test", {})
        assert ctx["widget"]["toolbar"] == ["bold", "italic"]

    def test_custom_height(self):
        widget = MarkdownEditorWidget(height="500px")
        ctx = widget.get_context("content", "test", {})
        assert ctx["widget"]["height"] == "500px"

    def test_default_height_from_settings(self):
        widget = MarkdownEditorWidget()
        ctx = widget.get_context("content", "test", {})
        assert ctx["widget"]["height"] == "300px"

    def test_custom_preview_url(self):
        widget = MarkdownEditorWidget(preview_url="/custom/preview/")
        ctx = widget.get_context("content", "test", {})
        assert ctx["widget"]["preview_url"] == "/custom/preview/"

    def test_custom_upload_url(self):
        widget = MarkdownEditorWidget(upload_url="/custom/upload/")
        ctx = widget.get_context("content", "test", {})
        assert ctx["widget"]["upload_url"] == "/custom/upload/"

    def test_default_placeholder(self):
        widget = MarkdownEditorWidget()
        ctx = widget.get_context("content", "", {})
        assert ctx["widget"]["placeholder"] == "Add your comment here..."

    def test_renders_without_error(self):
        widget = MarkdownEditorWidget()
        html = widget.render("content", "**hello**", {})
        assert "md-editor" in html
