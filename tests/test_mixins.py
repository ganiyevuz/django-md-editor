from unittest.mock import patch

from django.db.models import Model, TextField
from django.test import TestCase, override_settings

from django_md_editor.mixins import MarkdownCleanupMixin


# Define the test model once at module level to avoid re-registration warnings
class CleanupPost(MarkdownCleanupMixin, Model):
    content = TextField(default="")
    summary = TextField(default="")

    class Meta:
        app_label = "test"
        managed = False


class SelectiveCleanupPost(MarkdownCleanupMixin, Model):
    content = TextField(default="")
    summary = TextField(default="")
    markdown_cleanup_fields = ["content"]

    class Meta:
        app_label = "test"
        managed = False


def _make_instance(model_cls, pk=None, **field_values):
    """Create an instance without hitting the database."""
    instance = model_cls.__new__(model_cls)
    Model.__init__(instance)
    for key, val in field_values.items():
        setattr(instance, key, val)
    instance.pk = pk
    instance._md_original_values = instance._capture_markdown_fields()
    return instance


class MarkdownCleanupMixinTests(TestCase):
    def test_captures_all_text_fields_by_default(self):
        instance = _make_instance(
            CleanupPost,
            content="![img](/media/md-editor/uploads/2026/03/a.png)",
            summary="plain text",
        )
        assert "content" in instance._md_original_values
        assert "summary" in instance._md_original_values

    def test_captures_only_specified_fields(self):
        instance = _make_instance(
            SelectiveCleanupPost,
            content="text",
            summary="other",
        )
        assert "content" in instance._md_original_values
        assert "summary" not in instance._md_original_values

    @override_settings(MD_EDITOR={"CLEANUP_MEDIA": True})
    @patch("django_md_editor.mixins.delete_orphaned_media")
    def test_save_calls_cleanup_on_change(self, mock_cleanup):
        instance = _make_instance(
            CleanupPost,
            content="![img](/media/md-editor/uploads/2026/03/old.png)",
            pk=1,
        )
        instance.content = "new content"

        with patch.object(Model, "save"):
            instance.save()

        mock_cleanup.assert_called_once_with(
            "![img](/media/md-editor/uploads/2026/03/old.png)",
            "new content",
        )

    @override_settings(MD_EDITOR={"CLEANUP_MEDIA": True})
    @patch("django_md_editor.mixins.delete_orphaned_media")
    def test_save_skips_cleanup_for_new_objects(self, mock_cleanup):
        instance = _make_instance(
            CleanupPost,
            content="![img](/media/md-editor/uploads/2026/03/a.png)",
            pk=None,
        )

        with patch.object(Model, "save"):
            instance.save()

        mock_cleanup.assert_not_called()

    @override_settings(MD_EDITOR={"CLEANUP_MEDIA": False})
    @patch("django_md_editor.mixins.delete_orphaned_media")
    def test_save_skips_cleanup_when_disabled(self, mock_cleanup):
        instance = _make_instance(
            CleanupPost,
            content="![img](/media/md-editor/uploads/2026/03/old.png)",
            pk=1,
        )
        instance.content = "new content"

        with patch.object(Model, "save"):
            instance.save()

        mock_cleanup.assert_not_called()

    @override_settings(MD_EDITOR={"CLEANUP_MEDIA": True})
    @patch("django_md_editor.mixins.delete_orphaned_media")
    def test_save_skips_cleanup_when_unchanged(self, mock_cleanup):
        instance = _make_instance(
            CleanupPost,
            content="same content",
            pk=1,
        )

        with patch.object(Model, "save"):
            instance.save()

        mock_cleanup.assert_not_called()

    @override_settings(MD_EDITOR={"CLEANUP_MEDIA": True})
    @patch("django_md_editor.mixins.delete_orphaned_media")
    def test_save_updates_originals_after_save(self, mock_cleanup):
        instance = _make_instance(
            CleanupPost,
            content="old",
            pk=1,
        )
        instance.content = "new"

        with patch.object(Model, "save"):
            instance.save()

        assert instance._md_original_values["content"] == "new"
