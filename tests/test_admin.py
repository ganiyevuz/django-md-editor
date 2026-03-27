from unittest.mock import MagicMock

from django.contrib import admin
from django.db.models import CharField, Model, TextField
from django.test import TestCase

from django_markdown_widget.admin import MarkdownEditorAdminMixin
from django_markdown_widget.widgets import MarkdownEditorWidget


class FakeModel(Model):
    title = CharField(max_length=200)
    content = TextField()
    summary = TextField()

    class Meta:
        app_label = "test"


class AllFieldsAdmin(MarkdownEditorAdminMixin, admin.ModelAdmin):
    pass


class SelectiveFieldsAdmin(MarkdownEditorAdminMixin, admin.ModelAdmin):
    markdown_fields = ["content"]


class MarkdownEditorAdminMixinTests(TestCase):
    def test_all_textfields_get_widget_when_no_markdown_fields(self):
        model_admin = AllFieldsAdmin(FakeModel, admin.site)
        assert TextField in model_admin.formfield_overrides
        overrides = model_admin.formfield_overrides
        assert overrides[TextField]["widget"] is MarkdownEditorWidget

    def test_selective_fields_does_not_add_markdown_widget_to_overrides(self):
        model_admin = SelectiveFieldsAdmin(FakeModel, admin.site)
        tf_override = model_admin.formfield_overrides.get(TextField, {})
        assert tf_override.get("widget") is not MarkdownEditorWidget

    def test_selective_fields_overrides_matching_field(self):
        model_admin = SelectiveFieldsAdmin(FakeModel, admin.site)
        request = MagicMock()
        db_field = FakeModel._meta.get_field("content")
        formfield = model_admin.formfield_for_dbfield(db_field, request)
        assert isinstance(formfield.widget, MarkdownEditorWidget)

    def test_selective_fields_skips_non_matching_textfield(self):
        model_admin = SelectiveFieldsAdmin(FakeModel, admin.site)
        request = MagicMock()
        db_field = FakeModel._meta.get_field("summary")
        formfield = model_admin.formfield_for_dbfield(db_field, request)
        assert not isinstance(formfield.widget, MarkdownEditorWidget)

    def test_selective_fields_skips_non_textfield(self):
        model_admin = SelectiveFieldsAdmin(FakeModel, admin.site)
        request = MagicMock()
        db_field = FakeModel._meta.get_field("title")
        formfield = model_admin.formfield_for_dbfield(db_field, request)
        assert not isinstance(formfield.widget, MarkdownEditorWidget)
