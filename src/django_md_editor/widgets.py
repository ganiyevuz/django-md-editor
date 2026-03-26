import json

from django.forms.widgets import Textarea

from django_md_editor.settings import get_setting


class MarkdownEditorWidget(Textarea):
    template_name = "django_md_editor/widget.html"

    def __init__(
        self,
        toolbar=None,
        preview_url="/md-editor/preview/",
        upload_url="/md-editor/upload/",
        height=None,
        placeholder=None,
        attrs=None,
    ):
        self.toolbar = toolbar
        self.preview_url = preview_url
        self.upload_url = upload_url
        self.height = height
        self.placeholder = placeholder
        super().__init__(attrs=attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"]["toolbar"] = (
            self.toolbar if self.toolbar is not None else get_setting("TOOLBAR")
        )
        context["widget"]["toolbar_json"] = json.dumps(context["widget"]["toolbar"])
        context["widget"]["preview_url"] = self.preview_url
        context["widget"]["upload_url"] = self.upload_url
        context["widget"]["height"] = self.height or get_setting("DEFAULT_HEIGHT")
        context["widget"]["placeholder"] = (
            self.placeholder
            if self.placeholder is not None
            else get_setting("PLACEHOLDER")
        )
        context["widget"]["client_renderer"] = get_setting("CLIENT_RENDERER")
        context["widget"]["theme"] = get_setting("THEME")
        return context

    class Media:
        css = {"all": ("django_md_editor/css/editor.css",)}
        js = (
            "django_md_editor/js/marked.min.js",
            "django_md_editor/js/editor.js",
        )
