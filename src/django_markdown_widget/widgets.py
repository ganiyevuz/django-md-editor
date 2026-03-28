from __future__ import annotations

import json

from django.forms.widgets import Textarea

from django_markdown_widget.settings import get_setting


class MarkdownEditorWidget(Textarea):
    template_name = "django_markdown_widget/widget.html"

    def __init__(
        self,
        toolbar=None,
        upload_url="/md-editor/upload",
        finalize_url="/md-editor/finalize",
        height=None,
        placeholder=None,
        attrs=None,
    ):
        self.toolbar = toolbar
        self.upload_url = upload_url
        self.finalize_url = finalize_url
        self.height = height
        self.placeholder = placeholder
        super().__init__(attrs=attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"]["toolbar"] = (
            self.toolbar if self.toolbar is not None else get_setting("TOOLBAR")
        )
        context["widget"]["toolbar_json"] = json.dumps(
            context["widget"]["toolbar"]
        ).replace("</", r"<\/")
        context["widget"]["upload_url"] = self.upload_url
        context["widget"]["finalize_url"] = self.finalize_url
        context["widget"]["height"] = self.height or get_setting("DEFAULT_HEIGHT")
        context["widget"]["placeholder"] = (
            self.placeholder
            if self.placeholder is not None
            else get_setting("PLACEHOLDER")
        )
        context["widget"]["theme"] = get_setting("THEME")
        return context

    class Media:
        css = {"all": ("django_markdown_widget/css/editor.css",)}
        js = (
            "django_markdown_widget/js/markdown-it.min.js",
            "django_markdown_widget/js/markdown-it-mark.min.js",
            "django_markdown_widget/js/markdown-it-sub.min.js",
            "django_markdown_widget/js/markdown-it-sup.min.js",
            "django_markdown_widget/js/markdown-it-task-lists.min.js",
            "django_markdown_widget/js/highlight.min.js",
            "django_markdown_widget/js/editor.js",
        )
