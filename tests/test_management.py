from io import StringIO
from unittest.mock import MagicMock, patch

from django.core.management import call_command
from django.test import TestCase


class CleanupMarkdownMediaTests(TestCase):
    @patch(
        "django_md_editor.management.commands.cleanup_markdown_media.default_storage"
    )
    @patch("django_md_editor.management.commands.cleanup_markdown_media.apps")
    def test_dry_run_lists_without_deleting(self, mock_apps, mock_storage):
        mock_apps.get_models.return_value = []
        mock_storage.listdir.return_value = ([], ["orphan.png"])

        out = StringIO()
        call_command("cleanup_markdown_media", "--dry-run", stdout=out)

        output = out.getvalue()
        assert "dry-run" in output
        assert "orphan.png" in output
        mock_storage.delete.assert_not_called()

    @patch(
        "django_md_editor.management.commands.cleanup_markdown_media.default_storage"
    )
    @patch("django_md_editor.management.commands.cleanup_markdown_media.apps")
    def test_deletes_orphaned_files(self, mock_apps, mock_storage):
        mock_apps.get_models.return_value = []
        mock_storage.listdir.return_value = ([], ["orphan.png"])

        out = StringIO()
        call_command("cleanup_markdown_media", stdout=out)

        output = out.getvalue()
        assert "Deleted" in output
        mock_storage.delete.assert_called_once()

    @patch(
        "django_md_editor.management.commands.cleanup_markdown_media.default_storage"
    )
    @patch("django_md_editor.management.commands.cleanup_markdown_media.apps")
    def test_no_orphans_found(self, mock_apps, mock_storage):
        mock_apps.get_models.return_value = []
        mock_storage.listdir.return_value = ([], [])

        out = StringIO()
        call_command("cleanup_markdown_media", stdout=out)

        assert "No orphaned files" in out.getvalue()

    @patch(
        "django_md_editor.management.commands.cleanup_markdown_media.default_storage"
    )
    @patch("django_md_editor.management.commands.cleanup_markdown_media.apps")
    def test_handles_missing_upload_directory(self, mock_apps, mock_storage):
        mock_apps.get_models.return_value = []
        mock_storage.listdir.side_effect = FileNotFoundError

        out = StringIO()
        call_command("cleanup_markdown_media", stdout=out)

        assert "No upload directory" in out.getvalue()

    @patch(
        "django_md_editor.management.commands.cleanup_markdown_media.default_storage"
    )
    @patch("django_md_editor.management.commands.cleanup_markdown_media.apps")
    def test_keeps_referenced_files(self, mock_apps, mock_storage):
        # Set up a model with a TextField referencing a file
        mock_model = MagicMock()
        mock_model._meta.get_fields.return_value = [
            MagicMock(spec=["name"], name="content"),
        ]
        # Make isinstance(f, TextField) return True
        from django.db.models import TextField

        field = TextField()
        field.name = "content"
        mock_model._meta.get_fields.return_value = [field]

        mock_obj = MagicMock()
        mock_obj.content = "![img](/media/md-editor/uploads/2026/03/keep.png)"
        mock_model.objects.only.return_value.iterator.return_value = [mock_obj]

        mock_apps.get_models.return_value = [mock_model]
        mock_storage.listdir.return_value = (
            ["2026"],
            [],
        )

        # Simulate recursive listing
        def listdir_side_effect(path):
            if path == "md-editor/uploads/":
                return (["2026"], [])
            if path == "md-editor/uploads/2026/":
                return (["03"], [])
            if path == "md-editor/uploads/2026/03/":
                return ([], ["keep.png"])
            return ([], [])

        mock_storage.listdir.side_effect = listdir_side_effect

        out = StringIO()
        call_command("cleanup_markdown_media", stdout=out)

        assert "No orphaned files" in out.getvalue()
        mock_storage.delete.assert_not_called()
