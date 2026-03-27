from __future__ import annotations

from django.db.models import TextField

from django_markdown_widget.widgets import MarkdownEditorWidget


class MarkdownEditorAdminMixin:
    """Mixin for ModelAdmin that replaces all TextFields with MarkdownEditorWidget.

    Usage:
        class PostAdmin(MarkdownEditorAdminMixin, admin.ModelAdmin):
            pass

    To limit to specific fields:
        class PostAdmin(MarkdownEditorAdminMixin, admin.ModelAdmin):
            markdown_fields = ["content", "description"]
    """

    markdown_fields = None

    formfield_overrides_extra = {
        TextField: {"widget": MarkdownEditorWidget},
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not hasattr(self, "formfield_overrides"):
            self.formfield_overrides = {}
        if self.markdown_fields is None:
            self.formfield_overrides.update(self.formfield_overrides_extra)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if (
            self.markdown_fields is not None
            and isinstance(db_field, TextField)
            and db_field.name in self.markdown_fields
        ):
            kwargs["widget"] = MarkdownEditorWidget
        return super().formfield_for_dbfield(db_field, request, **kwargs)
